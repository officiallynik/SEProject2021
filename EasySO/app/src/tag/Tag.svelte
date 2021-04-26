<!--
  display tag search result svelte file
-->

<script>
  import { fade } from "svelte/transition";

  export let tagData;
</script>

<style>
  div {
    position: relative;
  }
  h1 {
    margin: 0;
    display: inline-flex;
    text-transform: capitalize;
    margin-top: 6px;
  }
  div span {
    color: var(--vscode-badge-foreground);
    padding: 0 5px;
    margin: 0 5px;
    border-radius: 2px;
    position: absolute;
  }
  .excerpt {
    border: 2px solid var(--vscode-textSeparator-foreground);
    padding: 10px;
  }
</style>

<div in:fade>

  {#if tagData.error_msg}
    <h2>{tagData.error_msg}</h2>
  {:else}
    <h1>about</h1>
    <span class="text-capitalize"><h1>{tagData.tag_name}</h1></span>

    <h3 class="text-capitalize">tag info</h3>

    <div class="excerpt">
      {@html tagData.excerpt}
    </div>

    {@html tagData.body}
  {/if}
</div>
