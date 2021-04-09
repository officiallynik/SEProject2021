function formatDate(dateAsUnix, i18n, type) {

  /**
   * type of date to display *[ excluded ]
   * search -  asked Jan 01 '19 *[ by user ]
   * question - asked Jan 01 '19 at 18:00
   * answer - answered Jan 01 '19 at 18:00
   * generic - *[ user ] Jan 01 '19 at 18:00
   */
  const unixDateConverted = new Date(dateAsUnix * 1000);
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  let prefix = "";
  let suffix = "";

  if (["search", "question"].includes(type)) {
    prefix = `asked `;
  } else if (type === "answer") {
    prefix = `answered `;
  }

  let year = `'${unixDateConverted.getFullYear().toString().substring(2, 4)}`;
  let month = unixDateConverted.getUTCMonth();
  let day = unixDateConverted.getUTCDate();
  day < 10 && (day = `0${day}`);

  if (type !== "generic") {
    const uctMinutes = unixDateConverted.getUTCMinutes();
    const minutes = uctMinutes < 10 ? `0${uctMinutes}` : uctMinutes;
    suffix = ` at ${unixDateConverted.getUTCHours()}:${minutes}`;
  }

  return `${prefix}${monthNames[month]} ${day} ${year}${suffix}`;

}

function timeAgo(timeAgo, i18n) {

  const unixTimeAgoConverted = new Date(timeAgo * 1000);
  const nowDate = new Date(Date.now());

  const utc2 = Date.UTC(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getMonth(), nowDate.getDate());
  const utc1 = Date.UTC(unixTimeAgoConverted.getFullYear(), unixTimeAgoConverted.getMonth(), unixTimeAgoConverted.getDate());

  const diff = utc2 - utc1;
  const diffInDays = Math.floor(diff / (1000 * 60 * 60 * 24));
  const diffInMonths = Math.floor(diff / (1000 * 60 * 60 * 24 * 30));
  const diffInYears = Math.floor(diff / (1000 * 60 * 60 * 24 * 30 * 12));

  let timeAgoFormatted;

  if (diffInYears > 1) {
    const months = Math.floor(diffInMonths / 12);
    switch (months) {
      case 0:
        timeAgoFormatted = `${diffInYears} years ago`
        break;
      case 1:
        timeAgoFormatted = `${diffInYears} years ${months} month ago`
        break;
      default: timeAgoFormatted = `${diffInYears} years ${months} months ago`
        break;
    }
  } else if (diffInMonths < 12 && diffInMonths > 1) {
    timeAgoFormatted = `${diffInMonths} months ago`
  } else if (diffInMonths === 1) {
    timeAgoFormatted = `${diffInMonths} month ago`
  } else if (diffInDays < 30 && diffInDays > 1) {
    timeAgoFormatted = `${diffInDays} days ago`
  } else if (diffInDays === 1) {
    timeAgoFormatted = `yesterday`
  } else {
    timeAgoFormatted = `today`
  }

  return timeAgoFormatted;
}

export { formatDate, timeAgo };