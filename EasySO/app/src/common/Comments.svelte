<!--
  display comments in questions and answers
-->
<script>
  export let comments;
  let commentsShowAmount = 5;

  $: commentsLength = comments && comments.length - commentsShowAmount - 1;

  function toggleComments() {
    commentsShowAmount = commentsShowAmount === 5 ? comments.length : 5;
  }
</script>

<style>
  section {
    padding-bottom: 20px;
    margin-top: 15px;
  }
  .container {
    display: table;
    border-bottom: 1px solid var(--vscode-textSeparator-foreground);
    width: 100%;
  }
  .container:last-of-type {
    border-bottom: 0;
    margin-bottom: 10px;
  }
  .container .col {
    display: table-cell;
    padding: 10px 0px 10px 10px;
  }
  .container .col:first-child {
    text-align: center;
    width: 30px;
    vertical-align: middle;
  }
  .container .col:last-child {
    text-align: left;
    word-break: keep-all;
  }
  .display-name {
    background-color: var(--vscode-textLink-foreground);
    color: var(--vscode-badge-foreground);
    padding: 0 4px 1px;
    font-size: 11px;
    word-break: keep-all;
  }
  .highlight-score {
    color: var(--vscode-textLink-foreground);
  }
</style>

<section>

  {#each comments as comment, i}
    {#if i <= commentsShowAmount}
      <div class="container">
        <div class="col">
          <strong class:highlight-score={comment.score > 9}>
            {#if comment.score === 0}-{:else}{comment.score}{/if}
          </strong>
        </div>
        <div class="col">
          {@html comment.body}
          <i>
            &nbsp;&nbsp;–&nbsp;&nbsp
            <span class="display-name">{comment.owner.display_name}</span>
            &nbsp {new Date(comment.creation_date * 1000).toDateString()}
          </i>
        </div>
      </div>
    {/if}
  {/each}

  <span class="link" on:click={toggleComments}>
    {#if comments.length > commentsShowAmount}
      {`show ${commentsLength} more comments`}
    {:else if comments.length === commentsShowAmount}
      hide comments
    {/if}
  </span>

</section>
