const vscode = acquireVsCodeApi();

/***
 * vscode api functions to change title and progress indication
 */
function vscodeProgress(action, title, hasError) {
  vscode.postMessage({
    command: "progress",
    action: action,
    title: title,
    error: hasError,
    errorMessage:
      "An error occured fetching results. Check your internet connection."
  });
}
function vscodeWindowTitle(title) {
  vscode.postMessage({
    command: "titleChange",
    title: `SO: ${title}`
  });
}

export { vscodeProgress, vscodeWindowTitle }