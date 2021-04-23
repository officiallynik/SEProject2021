<script>
  import { afterUpdate } from 'svelte';
  import Comments from "../common/Comments.svelte";
  import RowLayout from "../common/RowLayout.svelte";
  import ResultsBar from "../Common/ResultsBar.svelte";
  import Loader from "../Common/Loader.svelte";
  import User from "../Common/User.svelte";
  import Tags from "../Common/Tags.svelte";
  import QuestionAnswerIndicies from "./QuestionAnswerIndicies.svelte";

  export let questionId;
  export let answers;
  export let isAnswersLoading;

  afterUpdate(() => {
    const copyBtns = document.getElementsByClassName('copy-code-btn');
    for(let i=0; i<copyBtns.length; i++){
      copyBtns[i].parentElement.remove(copyBtns[i]);
    }

    const codeElements = document.getElementsByTagName('pre');
    for(let i=0; i<codeElements.length; i++){
      const copyBtn = document.createElement('button');
      copyBtn.innerHTML = "copy";
      copyBtn.classList.add("copy-code-btn");
      copyBtn.style.float = "right";
      copyBtn.style.display = "none";

      codeElements[i].id = `code-block-${i}`;
      copyBtn.onclick = function() {
        const code = document.getElementById(`code-block-${i}`).innerText;
        console.log("code", code);
      }

      codeElements[i].onmouseover = function () {
        copyBtn.style.display = "block";
      }

      codeElements[i].onmouseout = function () {
        copyBtn.style.display = "none";
      }
    }
  });
  
</script>

<style>
  section {
    border-bottom: 2px solid var(--vscode-textSeparator-foreground);
  }
  section:last-of-type {
    border-bottom: 0;
  }
  /* Duplicate styles from Questions.svelte */
  .question-answer-bottom {
    display: block;
    width: 100%;
    height: 82px;
  }
</style>

<ResultsBar
  {isAnswersLoading}
/>

{#if isAnswersLoading}
  <Loader />
{/if}

{#if answers}
  {#each answers as answer, i}
    <section>
      <RowLayout>

        <div slot="left">
          <QuestionAnswerIndicies
            score={answer.score}
            isAccepted={answer.is_accepted} />
        </div>

        <div slot="right">
          <div>
            {@html answer.body}
          </div>

          {#if answer.tags}
            <Tags tags={answer.tags} />
          {/if}

          <div class="question-answer-bottom">
            <User user={answer.owner} createdDate={answer.creation_date} />
          </div>

          {#if answer.comments}
            <Comments comments={answer.comments} />
          {/if}
        </div>
      </RowLayout>
    </section>
  {/each}
{/if}
