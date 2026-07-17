/**
 * Shared number/date formatters for Project Cortex UI.
 *
 * Single source of truth — import from here, never inline.
 */

/**
 * Format a number as Indian Rupees (en-IN locale, lakh notation).
 * e.g. formatINR(1800000) → "₹18,00,000"
 *      formatINR(0)       → "₹0"
 *
 * @param {number} amount
 * @returns {string}
 */
export function formatINR(amount) {
  if (typeof amount !== "number" || isNaN(amount)) return "₹0";
  return "₹" + Math.round(amount).toLocaleString("en-IN");
}

/**
 * Format a number as US Dollars.
 * e.g. formatUSD(42500) → "$42,500"
 *
 * @param {number} amount
 * @returns {string}
 */
export function formatUSD(amount) {
  if (typeof amount !== "number" || isNaN(amount)) return "$0";
  return "$" + Math.round(amount).toLocaleString("en-US");
}

/**
 * Pluralise a noun based on count.
 * e.g. pluralise(1, "day") → "1 day"
 *      pluralise(3, "day") → "3 days"
 *
 * @param {number} count
 * @param {string} noun
 * @returns {string}
 */
export function pluralise(count, noun) {
  return `${count} ${noun}${count === 1 ? "" : "s"}`;
}
