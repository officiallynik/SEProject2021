<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { page, searchQuery } from "../stores/common.js";
  import SearchTips from "./SearchTips.svelte";

  let showTips = false;
  export let tagData;
  export let isLoading;
  export let showInstructions;
  let searchQueryPreviousValue;

  function toggleSearchTips() {
    showTips = !showTips;
  }

  onMount(() => {
    searchQueryPreviousValue = $searchQuery;
  });

  $: isLoading && (searchQueryPreviousValue = $searchQuery);

  function handleSearchByEnterKey(event) {
    if (event.keyCode === 13) {
      handleSearch();
    }
  }

  function handleSearch() {
    if (
      !isLoading &&
      $searchQuery !== searchQueryPreviousValue &&
      $searchQuery !== ""
    ) {
      search();
    }
  }

  const dispatch = createEventDispatcher();
  function search() {
    searchQueryPreviousValue = $searchQuery;
    dispatch("searchInput");
  }

</script>

<svelte:window on:keydown={handleSearchByEnterKey} />

<section>
  <div class="text-capitalize">
    Showing Results for
    <strong>
      <i>
        {#if tagData && tagData.tag_name}
          {tagData.tag_name}
        {:else if searchQueryPreviousValue}
          {searchQueryPreviousValue}
        {/if}
      </i>
    </strong>

    {#if !showInstructions}
    <span
      class="link advanced-search-tips link-search"
      on:click={toggleSearchTips}
    >
      {#if !showTips}
        Search Tips
      {:else}Close Tips{/if}
    </span>
    {/if}
  </div>

  <input type="text" bind:value={$searchQuery} />

  <button on:click={handleSearch} class="text-capitalize"> Search </button>

  <div on:click={handleSearch} class="link link-search">
    Stack Overflow Direct Search
  </div>
</section>

{#if showTips || showInstructions}
  <h3>Search Tips</h3>
  <SearchTips />
{/if}

<style>
  section {
    display: block;
    margin-top: 24px;
  }
  section div {
    margin-bottom: 0;
    display: block;
  }
  section input {
    background-color: var(--vscode-input-background);
    box-shadow: 0 0 0 1px var(--vscode-input-border);
    color: var(--vscode-input-foreground);
    border: 0;
    border-radius: 2px;
    margin: 8px 5px 12px 0;
    padding: 5px;
    height: 17px;
    width: calc(100% - 120px);
  }
  section button {
    min-width: 100px;
    max-width: 100px;
  }

  .advanced-search-tips {
    float: right;
  }

  .link-search {
    color: var(--vscode-textLink-foreground);
    user-select: none;
    opacity: 0.8;
  }
  .link-search:hover {
    opacity: 1;
  }

</style>
