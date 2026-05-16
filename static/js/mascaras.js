var cleave = new Cleave("#numero", {
  delimiters: ["(", ") ", "-"],
  blocks: [0, 2, 5, 4],
  numericOnly: true,
});

var cleave = new Cleave("#data", {
  date: true,
  delimiter: "/",
  datePattern: ["d", "m", "Y"],
});

var cleave = new Cleave("#hora", {
  time: true,
  timePattern: ["h", "m"],
});
