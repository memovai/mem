import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from memov.core.git import GitManager

LOGGER = logging.getLogger(__name__)


class TraceExporter:
    """Export memov history to trace.json format"""

    def __init__(self, project_path: str):
        """Initialize the TraceExporter"""
        self.project_path = project_path
        self.bare_repo_path = os.path.join(project_path, ".mem", "memov.git")
        self.branches_config_path = os.path.join(project_path, ".mem", "branches.json")

    def _load_branches(self) -> Optional[Dict]:
        """Load branches configuration from the branches config file."""
        if not os.path.exists(self.branches_config_path):
            return None

        with open(self.branches_config_path, "r") as f:
            return json.load(f)

    def _extract_operation_type(self, commit_message: str) -> str:
        """Extract operation type from commit message first line."""
        if not commit_message:
            return "unknown"

        first_line = commit_message.splitlines()[0].lower()

        if "track" in first_line:
            return "track"
        elif "snapshot" in first_line or "snap" in first_line:
            return "snap"
        elif "rename" in first_line:
            return "rename"
        elif "remove" in first_line:
            return "remove"
        elif "amend" in first_line:
            return "amend"
        else:
            return "unknown"

    def _parse_commit_message(self, commit_message: str) -> Dict[str, Any]:
        """Parse commit message to extract prompt, response, and other metadata."""
        result = {
            "prompt": None,
            "response": None,
            "source": "ai",
            "files": [],
            "old_path": None,
            "new_path": None,
            "file_path": None,
        }

        lines = commit_message.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("Prompt:"):
                result["prompt"] = line[len("Prompt:") :].strip()
            elif line.startswith("Response:"):
                result["response"] = line[len("Response:") :].strip()
            elif line.startswith("Source:"):
                source = line[len("Source:") :].strip()
                result["source"] = "user" if source.lower() == "user" else "ai"
            elif line.startswith("Files:"):
                files_str = line[len("Files:") :].strip()
                if "->" in files_str:  # Rename operation
                    parts = files_str.split("->")
                    if len(parts) == 2:
                        result["old_path"] = parts[0].strip()
                        result["new_path"] = parts[1].strip()
                else:  # Track/remove operation
                    files = [f.strip() for f in files_str.split(",")]
                    result["files"] = files
                    if len(files) == 1:  # Single file operation
                        result["file_path"] = files[0]

        return result

    def _get_commit_diff(self, commit_hash: str) -> Optional[str]:
        """Get the diff content of a specific commit."""
        try:
            diff_content = GitManager.get_commit_diff(self.bare_repo_path, commit_hash)
            if diff_content:
                # Parse the diff content to extract only the diff part (after the commit info)
                lines = diff_content.split("\n")
                diff_start = -1

                # Find where the actual diff starts (after commit info)
                for i, line in enumerate(lines):
                    if line.startswith("diff --git"):
                        diff_start = i
                        break

                if diff_start >= 0:
                    # Return only the diff part
                    return "\n".join(lines[diff_start:])
                else:
                    # If no diff found, return None (not the full content)
                    return None

        except Exception as e:
            LOGGER.debug(f"Failed to get diff for commit {commit_hash}: {e}")

        return None

    def _get_commit_timestamp(self, commit_hash: str) -> str:
        """Get commit timestamp in ISO format."""
        try:
            timestamp = GitManager.get_commit_timestamp(self.bare_repo_path, commit_hash)
            if timestamp:
                return timestamp
        except Exception as e:
            LOGGER.debug(f"Failed to get commit timestamp: {e}")

        # Fallback to current time
        return datetime.now().isoformat()

    def _get_branch_for_commit(self, commit_hash: str, branches: Dict) -> str:
        """Get branch name for a specific commit."""
        try:
            # Find which branch this commit belongs to
            for branch_name, branch_commit in branches["branches"].items():
                # Check if this commit is in the history of this branch
                commit_history = GitManager.get_commit_history(self.bare_repo_path, branch_commit)
                if commit_hash in commit_history:
                    return branch_name
        except Exception as e:
            LOGGER.debug(f"Failed to get branch for commit {commit_hash}: {e}")

        return "unknown"

    def _get_parent_branch_info(self, commit_hash: str, branches: Dict) -> Optional[Dict[str, str]]:
        """Get parent branch information for a commit that creates a new branch."""
        try:
            # Get commit parent
            parent_commit = GitManager.get_commit_parent(self.bare_repo_path, commit_hash)
            if parent_commit:
                # Find which branch the parent commit belongs to
                for branch_name, branch_commit in branches["branches"].items():
                    commit_history = GitManager.get_commit_history(self.bare_repo_path, branch_commit)
                    if parent_commit in commit_history:
                        return {"parent_branch": branch_name, "parent_commit": parent_commit}
        except Exception as e:
            LOGGER.debug(f"Failed to get parent branch info for commit {commit_hash}: {e}")

        return None

    def export_trace(self, output_path: Optional[str] = None) -> str:
        """Export memov history to trace.json format"""
        try:
            # Load branches configuration
            branches = self._load_branches()
            if branches is None:
                raise Exception("No branches found in memov repo. Please initialize or track files first.")

            trace_data = []

            # Get all commits from all branches
            all_commits = set()
            for branch_name, branch_commit in branches["branches"].items():
                commit_history = GitManager.get_commit_history(self.bare_repo_path, branch_commit)
                all_commits.update(commit_history)

            # Process each commit
            for commit_hash in sorted(all_commits):
                try:
                    # Get commit message
                    commit_message = GitManager.get_commit_message(self.bare_repo_path, commit_hash)
                    if not commit_message:
                        continue

                    # Extract operation type
                    operation = self._extract_operation_type(commit_message)

                    # Parse commit message for metadata
                    metadata = self._parse_commit_message(commit_message)

                    # Get branch for this commit
                    branch = self._get_branch_for_commit(commit_hash, branches)

                    # Get timestamp
                    timestamp = self._get_commit_timestamp(commit_hash)

                    # Get parent branch information
                    parent_info = self._get_parent_branch_info(commit_hash, branches)

                    # Create trace entry
                    trace_entry = {
                        "timestamp": timestamp,
                        "operation": operation,
                        "branch": branch,
                        "prompt": metadata["prompt"],
                        "response": metadata["response"],
                        "source": metadata["source"],
                        "commit_hash": commit_hash,
                    }

                    # Add parent branch information if available
                    if parent_info:
                        trace_entry["parent_branch"] = parent_info["parent_branch"]
                        trace_entry["parent_commit"] = parent_info["parent_commit"]
                    else:
                        trace_entry["parent_branch"] = None

                    # Add operation-specific fields
                    if metadata["files"]:
                        trace_entry["files"] = metadata["files"]
                    if metadata["old_path"]:
                        trace_entry["old_path"] = metadata["old_path"]
                    if metadata["new_path"]:
                        trace_entry["new_path"] = metadata["new_path"]
                    if metadata["file_path"]:
                        trace_entry["file_path"] = metadata["file_path"]

                    # Add diff for operations that modify files
                    diff_operations = ["track", "snap", "rename", "remove"]
                    if operation in diff_operations:
                        diff = self._get_commit_diff(commit_hash)
                        if diff:
                            trace_entry["diff"] = diff

                    trace_data.append(trace_entry)

                except Exception as e:
                    LOGGER.warning(f"Failed to process commit {commit_hash}: {e}")
                    continue

            # Sort by timestamp
            trace_data.sort(key=lambda x: x["timestamp"])

            # Determine output path
            if output_path is None:
                output_path = os.path.join(self.project_path, "trace.json")

            # Write to file
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(trace_data, f, ensure_ascii=False, indent=2)

            LOGGER.info(f"Exported {len(trace_data)} trace records to {output_path}")
            return output_path

        except Exception as e:
            LOGGER.error(f"Failed to export trace: {e}")
            raise
