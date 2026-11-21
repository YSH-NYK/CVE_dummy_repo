/**
 * Demo Node.js service using vulnerable dependencies for CVE Fixer testing.
 */

const _ = require("lodash");
const axios = require("axios");
const underscore = require("underscore");

console.log("CVE Dummy Node.js Service starting...");

// Demonstrate lodash usage
const rawData = [
  { id: 1, name: "Alice", group: "admin" },
  { id: 2, name: "Bob", group: "dev" },
  { id: 3, name: "Charlie", group: "dev" },
];

const grouped = _.groupBy(rawData, "group");
console.log("Grouped data (lodash):", JSON.stringify(grouped));

// Demonstrate underscore usage
const mapped = underscore.map(rawData, (item) => item.name);
console.log("User names (underscore):", mapped);

// Demonstrate axios usage
async function checkService() {
  try {
    const res = await axios.get("https://httpbin.org/status/200", { timeout: 3000 });
    console.log("Axios test response status:", res.status);
  } catch (err) {
    console.log("Axios test finished (offline or mocked).");
  }
}

checkService();
