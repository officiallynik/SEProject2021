<!--
  search input box, tips trigger svelte file
-->
<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { searchQuery } from "../stores/common.js";
  import Tags from "../common/Tags.svelte";
  import SearchTips from "./SearchTips.svelte";

  let showTips = false;
  export let tagData;
  export let isLoading;
  export let initialInstruction;
  export let errorObj;
  let searchQueryPreviousValue;
  let searchType = "PyStackBot";

  function selectSearchType() {
    let w = document.getElementById("searchType").selectedIndex;
    let type = document.getElementById("searchType").options[w].value;

    searchType = type;
  }

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
      !isLoading
    ) {
      search();
    }
  }

  const dispatch = createEventDispatcher();
  function search() {
    searchQueryPreviousValue = $searchQuery;
    if(searchType === "PyStackBot"){
      dispatch("searchPyStackBot");
    }
    else {
      dispatch("searchSO");
    }
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

    {#if !initialInstruction}
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

  <div class="search-type">
    <label for="searchType">Search Type:</label>
    <select name="searchType" id="searchType" on:change={selectSearchType}>
      <option value="PyStackBot">PyStackBot</option>
      <option value="SO">Stack Overflow</option>
    </select>
  </div>

  <input type="text" bind:value={$searchQuery} />

  <button on:click={handleSearch} class="text-capitalize"> Search </button>
</section>

{#if initialInstruction || showTips}
  <h3>Search Tips</h3>
  <SearchTips />
{/if}

{#if errorObj !== null}
    <div class="errorBox">
      <div class="errorType">
        Error Type
        <Tags tags={[errorObj.errorType]} on:searchByTag />
      </div>
      <div class="errorInfo">
        {@html errorObj.errorInfo}
      </div>
      <div class="errorTip">
        Tip: Install python linter, it helps reduce errors (eg: NameError, ImportError etc) during development. 
      </div>
    </div>
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

  .errorBox {
    margin-top: 10px;
    border: 1px solid var(--vscode-input-foreground);
    padding: 10px;
  }

  .errorInfo {
    font-size: 16px;
    margin-top: 10px;
  }

  .errorTip {
    margin-top: 10px;
  }

  .search-type {
    margin-top: 5px;
  }

  .search-type select {
    background-color: var(--vscode-input-background);
    color: var(--vscode-input-foreground);
  }

</style>
