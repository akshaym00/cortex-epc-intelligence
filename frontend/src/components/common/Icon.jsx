import React from "react";

const icons = {
  building: [["path", { d: "M3 21h18" }], ["path", { d: "M5 21V5a2 2 0 0 1 2-2h7v18" }], ["path", { d: "M14 8h3a2 2 0 0 1 2 2v11" }], ["path", { d: "M8 7h2" }], ["path", { d: "M8 11h2" }], ["path", { d: "M8 15h2" }]],
  package: [["path", { d: "m7.5 4.27 9 5.15" }], ["path", { d: "M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z" }], ["path", { d: "m3.3 7 8.7 5 8.7-5" }], ["path", { d: "M12 22V12" }]],
  shield: [["path", { d: "M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V5l8-3 8 3Z" }], ["path", { d: "m9 12 2 2 4-5" }]],
  branch: [["path", { d: "M6 3v12" }], ["circle", { cx: "18", cy: "6", r: "3" }], ["circle", { cx: "6", cy: "18", r: "3" }], ["path", { d: "M18 9a9 9 0 0 1-9 9" }]],
  fileCheck: [["path", { d: "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z" }], ["path", { d: "M14 2v6h6" }], ["path", { d: "m9 15 2 2 4-4" }]],
  alert: [["path", { d: "m21.7 18-8-14a2 2 0 0 0-3.4 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3" }], ["path", { d: "M12 9v4" }], ["path", { d: "M12 17h.01" }]],
  calendar: [["path", { d: "M8 2v4" }], ["path", { d: "M16 2v4" }], ["rect", { x: "3", y: "4", width: "18", height: "18", rx: "2" }], ["path", { d: "M3 10h18" }]],
  clock: [["circle", { cx: "12", cy: "12", r: "10" }], ["path", { d: "M12 6v6l4 2" }]],
  users: [["path", { d: "M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" }], ["circle", { cx: "9", cy: "7", r: "4" }], ["path", { d: "M22 21v-2a4 4 0 0 0-3-3.87" }], ["path", { d: "M16 3.13a4 4 0 0 1 0 7.75" }]],
  hardDrive: [["line", { x1: "22", x2: "2", y1: "12", y2: "12" }], ["path", { d: "M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" }], ["line", { x1: "6", x2: "6.01", y1: "16", y2: "16" }], ["line", { x1: "10", x2: "10.01", y1: "16", y2: "16" }]],
  check: [["path", { d: "M20 6 9 17l-5-5" }]],
};

function Icon({ name = "fileCheck", size = 18 }) {
  return (
    <svg className="icon" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {(icons[name] || icons.fileCheck).map(([Tag, props], index) => (
        <Tag key={index} {...props} />
      ))}
    </svg>
  );
}

export default Icon;
