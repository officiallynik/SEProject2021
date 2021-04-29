export default function createCopyBtn(id) {
    const copyBtn = document.createElement('button');
    copyBtn.id = id;
    copyBtn.classList.add("copy-btn");
    
    copyBtn.innerText = "copy";

    copyBtn.style.float = "right";

    return copyBtn;
}