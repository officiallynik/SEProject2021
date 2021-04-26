/** 
 * main extension file, listen for inputs and creates webviews by implementing other files
*/

import * as vscode from 'vscode';
import { posix } from 'path';
import { AppPageHtml } from './app-page';
import GeneratorQuery from './generate-query';
import { pythonErrors } from './utils';

/* function to activate extension */
export function activate(context: vscode.ExtensionContext) {

  // store existing panel created, to reuse instead of creating new one
  let existingPanel: vscode.WebviewPanel|null = null;

  // normal search, error search using keybindings and text input
  let searchWithTextBox = vscode.commands.registerCommand('extension.searchWithTextBox', (errorObj) => {

    const editor = vscode.window.activeTextEditor;
    let searchQuery = "";
    
    if (editor) {
      searchQuery = editor.document.getText(editor.selection);
    }
    if(errorObj){
      searchQuery = errorObj;
    }

    if (existingPanel) {
      existingPanel.webview.postMessage({
        action: 'search',
        query: searchQuery,
        language: "English",
        sortType: "Relevance"
      });

      return;
    }

    const currentLanguageSelection = vscode.workspace.getConfiguration().get('English');

    const currentSortTypeSelection = vscode.workspace.getConfiguration().get('Relevance');

    const stackoverflowPanel = createWebViewPanel("EasySO", context.extensionPath);
    existingPanel = stackoverflowPanel;

    stackoverflowPanel.webview.html = AppPageHtml(context.extensionPath, stackoverflowPanel);

    if(!errorObj){
      stackoverflowPanel.webview.postMessage({
        action: 'search',
        query: searchQuery,
        language: currentLanguageSelection,
        sortType: currentSortTypeSelection
      });
    }
    else {
      stackoverflowPanel.webview.postMessage({
        action: 'searchError',
        query: searchQuery,
        language: currentLanguageSelection,
        sortType: currentSortTypeSelection
      });
    }

    // run on dispose
    stackoverflowPanel.onDidDispose(() => {
      existingPanel = null;
    });

    // Show progress loader
    windowProgress(stackoverflowPanel);

    // Listen for changes to window title
    changeWindowTitle(stackoverflowPanel);
  });

  // invoke error search on python files using keybindings
  let searchTerminalErrors = vscode.commands.registerCommand('extension.searchTerminalErrors', () => {

    if(!vscode.window.activeTerminal) {
      vscode.window.showErrorMessage("No Terminal Found");
      return;
    }

    const createError = (text:Array<string>) => {
      let errorLine = -1;
      let errorType = "";
      
      text.forEach((line, lineNumber) => {
        let errorList = line.match(/.*Error/g)
        if(errorList){
          errorLine = lineNumber;
          errorType = errorList[0];
        }
      })

      if(errorLine === -1){
        return null;
      }
      
      const error = text[errorLine];
      const errorInfo = pythonErrors[errorType];
      let fileName = text[errorLine-2].match(/".*"/g)![0];
      fileName = fileName.slice(1, fileName.length-1);
      const lineNumber = text[errorLine-2].match(/line \d*/g)![0];

      return {
        error,
        errorType,
        errorInfo,
        fileName,
        lineNumber
      };
    }

    var clipboard_content:string = "";

    vscode.commands.executeCommand('workbench.action.terminal.selectToPreviousCommand').then(() => {
      vscode.commands.executeCommand('workbench.action.terminal.copySelection').then(() => {
        vscode.commands.executeCommand('workbench.action.terminal.clearSelection').then(async () => {

          clipboard_content = await vscode.env.clipboard.readText();

          let isPython = clipboard_content.match(/.*python.*/g);
          if(isPython === null){
            vscode.window.showErrorMessage("Python Execution Not Found, Use 'python(3) <filename>.py' To Execute");
            return;
          }
          
          const text = clipboard_content.split("\n");
          const errorObj = createError(text);
          if(!errorObj){
            vscode.window.showInformationMessage("No Error Found, Python Executed Without Errors");
            return;
          }

          if(existingPanel) {
            existingPanel.webview.postMessage({
              action: 'searchError',
              query: errorObj,
              language: "English",
              sortType: "Relevance"
            });

            return;
          }

          vscode.commands.executeCommand('extension.searchWithTextBox', errorObj);
          
        });
      });
    });

  });

  // invoke extension using keybindings and generate query automatically
  let searchWithAutoQuery = vscode.commands.registerCommand('extension.searchWithAutoQuery', () => {

    const editor = vscode.window.activeTextEditor;
    let searchQuery = "";
    
    if (editor) {
      const fileType = editor.document.fileName.slice(editor.document.fileName.length-2).toLowerCase();
      if(fileType !== "py") {
        vscode.window.showErrorMessage("Auto query only works on python files for now :(");
        return;
      }

      console.log(editor.document.getText(editor.selection))
      searchQuery = "python" + GeneratorQuery(editor.document.getText(editor.selection));
    }
    else {
      vscode.window.showErrorMessage("Auto query only works if text is selected in python file editor");
      return;
    }

    if (existingPanel) {
      existingPanel.webview.postMessage({
        action: 'search',
        query: searchQuery,
        language: "English",
        sortType: "Relevance"
      });
      return;
    }

    const currentLanguageSelection = vscode.workspace.getConfiguration().get('English');

    const currentSortTypeSelection = vscode.workspace.getConfiguration().get('Relevance');

    const stackoverflowPanel = createWebViewPanel("EasySO", context.extensionPath);
    existingPanel = stackoverflowPanel;

    stackoverflowPanel.webview.html = AppPageHtml(context.extensionPath, stackoverflowPanel);

    stackoverflowPanel.webview.postMessage({
      action: 'search',
      query: searchQuery,
      language: currentLanguageSelection,
      sortType: currentSortTypeSelection
    });

    // run on dispose
    stackoverflowPanel.onDidDispose(() => {
      existingPanel = null;
    });

    // Show progress loader
    windowProgress(stackoverflowPanel);

    // Listen for changes to window title
    changeWindowTitle(stackoverflowPanel);
  });
 
  context.subscriptions.push(searchWithTextBox);
  context.subscriptions.push(searchTerminalErrors);
  context.subscriptions.push(searchWithAutoQuery);
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

/**
 * windowProgress - show progress in notification bar on message
 * @param panel webpanel
 */
function windowProgress(panel: vscode.WebviewPanel) {
  panel.webview.onDidReceiveMessage(message => {
    if (message.command === 'progress' && message.action === 'start') {
      showWindowProgress(panel, message.title);
    }
  });
}

/**
 * showWindowProgress - show progress in notification bar
 * @param panel webpanel
 * @param title string
 */
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

// run on extension deactivate
export function deactivate() { }