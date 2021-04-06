<script>
  import { onDestroy } from "svelte";
  // import { i18n, languages } from "../stores/i18n.js";
  // import { formatNumber, section } from "../stores/common.js";
  import {
    resultFilters,
    selectedAnswerFilter
  } from "../stores/results-filter.js";

  export let results;
  export let isLoading;

  // $: total = formatNumber(results);
  // $: title = $section === "search" ? $i18n.text.results : $i18n.text.answers;
  // $: titleForNoResults =
  //   $section === "search" ? $i18n.text.no_results_found : $i18n.text.no_answers;
</script>

<style>
  section {
    border-bottom: 2px solid var(--vscode-textSeparator-foreground);
    display: flex;
    align-items: center;
  }
  div:first-of-type {
    width: 30%;
  }
  div:first-of-type header {
    margin: 10px 0;
    font-size: 16px;
  }
  div:last-of-type {
    width: 70%;
    text-align: right;
  }
  .link-questions {
    color: var(--vscode-textLink-foreground);
    user-select: none;
    opacity: 0.8;
  }
  .link-questions:hover {
    opacity: 1;
  }
</style>

<section>

  <div>
    <h2>
      Top Results
      <!-- {#if results > 0}
        {total} {title}
      {:else if results === 0}{titleForNoResults}{:else if isLoading}&nbsp;{/if} -->
    </h2>

  </div>
  <div class="link link-questions">
    View Related Questions
  </div>
</section>
