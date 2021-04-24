<script>
  import { section } from "../stores/common.js";
  import { createEventDispatcher } from "svelte";

  export let extensionAction;

  const dispatch = createEventDispatcher();
  function goBack() {
    dispatch("goBack");
  }
</script>

<style>
  h3 {
    font-weight: normal;
    color: var(--vscode-textLink-foreground);
    margin: 0;
  }
  .back {
    cursor: pointer;
  }
  .back span::before {
    border-style: solid;
    border-width: 2px 2px 0 0;
    content: "";
    display: inline-block;
    height: 0.45em;
    left: 0;
    position: relative;
    top: 6px;
    transform: rotate(-135deg);
    vertical-align: top;
    width: 0.45em;
    cursor: pointer;
  }
  small {
    color: var(--vscode-textLink-foreground);
    margin-left: 12px;
  }
</style>

<h3 class="text-capitalize">
  {#if ($section === 'question' && extensionAction === 'search') || $section === 'tag'}
    <div class="back text-capitalize" on:click={goBack}>
      {#if $section === 'tag'}
        <span />
        Back to Search
      {:else}
        <span />
        Back to Questions
      {/if}
    </div>
  {:else}
    <strong>Easy StackOverflow</strong>
  {/if}
</h3>
