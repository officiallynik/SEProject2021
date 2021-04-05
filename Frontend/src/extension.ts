import * as vscode from 'vscode';
import { posix } from 'path';
import { AppPageHtml } from './app-page';

export function activate(context: vscode.ExtensionContext) {

  let searchPyStackBot = vscode.commands.registerCommand('extension.searchPyStackBot', () => {

    // Search options
    const searchOptions: vscode.InputBoxOptions = {
      placeHolder: 'Search',
      prompt: '*Required',
    };

    // Show Input
    vscode.window.showInputBox(searchOptions).then((searchQuery: string | undefined) => {

      if (searchQuery) {

        // Get language
        const currentLanguageSelection = vscode.workspace.getConfiguration().get('English');
        // Get sort type
        const currentSortTypeSelection = vscode.workspace.getConfiguration().get('Relevance');
        // Create webview panel
        const stackoverflowPanel = createWebViewPanel("PyStackBot", context.extensionPath);
        // Set webview - svelte - built to ./app/public/*
        stackoverflowPanel.webview.html = AppPageHtml(context.extensionPath, stackoverflowPanel);
        // Post search term, read in App.svelte as window.addEventListener("message"
        stackoverflowPanel.webview.postMessage({
          action: 'search',
          query: searchQuery,
          language: currentLanguageSelection,
          sortType: currentSortTypeSelection
        });

        // Show progress loader
        windowProgress(stackoverflowPanel);

        // Listen for changes to window title
        changeWindowTitle(stackoverflowPanel);

      }

    });
  });


  context.subscriptions.push(searchPyStackBot);
}

/**
 * Create vscode webViewPanel - sets default html with connection to /app
 * @param panelTitle string
 * @param path string
 */
function createWebViewPanel(panelTitle: string, path: string): vscode.WebviewPanel {
  return vscode.window.createWebviewPanel('webview', panelTitle, vscode.ViewColumn.Beside, {
    localResourceRoots: [vscode.Uri.file(posix.join(path, 'app', 'public'))],
    enableScripts: true,
    retainContextWhenHidden: true
  });
}

function windowProgress(panel: vscode.WebviewPanel) {
  panel.webview.onDidReceiveMessage(message => {
    if (message.command === 'progress' && message.action === 'start') {
      showWindowProgress(panel, message.title);
    }
  });
}

function showWindowProgress(panel: vscode.WebviewPanel, title: string) {
  vscode.window.withProgress({
    location: vscode.ProgressLocation.Window,
    title: title
  }, (progress, token) => {

    const progressPromise = new Promise<void>(resolve => {
      panel.webview.onDidReceiveMessage(message => {

        if (message.command === 'progress' && message.action === 'stop') {
          resolve();
          if (message.error) {
            vscode.window.showErrorMessage(message.errorMessage);
          }
        }

      });
    });

    return progressPromise;

  });
}

/**
 * Change window title based on user actions in the app
 * @param panel webview panel
 */
function changeWindowTitle(panel: vscode.WebviewPanel) {
  panel.webview.onDidReceiveMessage(message => {
    if (message.command === 'titleChange') {
      panel.title = message.title;
    }
  });
}

export function deactivate() { }