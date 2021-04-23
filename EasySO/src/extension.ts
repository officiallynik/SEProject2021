import * as vscode from 'vscode';
import { posix } from 'path';
import { AppPageHtml } from './app-page';
import GeneratorQuery from './generate-query';

export function activate(context: vscode.ExtensionContext) {

  let existingPanel: vscode.WebviewPanel|null = null;

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

  let searchTerminalErrors = vscode.commands.registerCommand('extension.searchTerminalErrors', () => {

    if(!vscode.window.activeTerminal) {
      vscode.window.showErrorMessage("No Terminal Found");
      return;
    } 

    const pythonErrors: { [key: string]: string } = {
      "AssertionError": "Raised when an <code>assert</code> statement fails.",
      "AttributeError": "Raised when attribute assignment or reference fails.",
      "EOFError": "Raised when the <code>input()</code> function hits end-of-file condition.",
      "FloatingPointError": "Raised when a floating point operation fails.",
      "GeneratorExit": "Raise when a generator's <code>close()</code> method is called.",
      "ImportError": "Raised when the imported module is not found.",
      "IndexError": "Raised when the index of a sequence is out of range.",
      "KeyError": "Raised when a key is not found in a dictionary.",
      "KeyboardInterrupt": "Raised when the user hits the interrupt key (<code>Ctrl+C</code> or <code>Delete</code>).",
      "MemoryError": "Raised when an operation runs out of memory.",
      "NameError": "Raised when a variable is not found in local or global scope.",
      "NotImplementedError": "Raised by abstract methods.",
      "OSError": "Raised when system operation causes system related error.",
      "OverflowError": "Raised when the result of an arithmetic operation is too large to be represented.",
      "ReferenceError": "Raised when a weak reference proxy is used to access a garbage collected referent.",
      "RuntimeError": "Raised when an error does not fall under any other category.",
      "StopIteration": "Raised by <code>next()</code> function to indicate that there is no further item to be returned by iterator.",
      "SyntaxError": "Raised by parser when syntax error is encountered.",
      "IndentationError": "Raised when there is incorrect indentation.",
      "TabError": "Raised when indentation consists of inconsistent tabs and spaces.",
      "SystemError": "Raised when interpreter detects internal error.",
      "SystemExit": "Raised by <code>sys.exit()</code> function.",
      "TypeError": "Raised when a function or operation is applied to an object of incorrect type.",
      "UnboundLocalError": "Raised when a reference is made to a local variable in a function or method, but no value has been bound to that variable.",
      "UnicodeError": "Raised when a Unicode-related encoding or decoding error occurs.",
      "UnicodeEncodeError": "Raised when a Unicode-related error occurs during encoding.",
      "UnicodeDecodeError": "Raised when a Unicode-related error occurs during decoding.",
      "UnicodeTranslateError": "Raised when a Unicode-related error occurs during translating.",
      "ValueError": "Raised when a function gets an argument of correct type but improper value.",
      "ZeroDivisionError": "Raised when the second operand of division or modulo operation is zero."
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

          vscode.commands.executeCommand('extension.searchPyStackBot', errorObj);
          
        });
      });
    });

  });

  let searchWithAutoQuery = vscode.commands.registerCommand('extension.searchWithAutoQuery', (errorObj) => {

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