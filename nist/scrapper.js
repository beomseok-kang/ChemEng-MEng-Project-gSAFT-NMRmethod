delete compound, colToArr, array, availables, windows;

var compound = prompt("Compound Name:");

(function (console) {
  console.save = function (data, filename) {
    if (!data) {
      console.error("Console.save: No data");
      return;
    }

    if (!filename) filename = "console.json";

    if (typeof data === "object") {
      data = JSON.stringify(data, undefined, 4);
    }

    var blob = new Blob([data], { type: "text/json" }),
      e = document.createEvent("MouseEvents"),
      a = document.createElement("a");

    a.download = filename;
    a.href = window.URL.createObjectURL(blob);
    a.dataset.downloadurl = ["text/json", a.download, a.href].join(":");
    e.initMouseEvent(
      "click",
      true,
      false,
      window,
      0,
      0,
      0,
      0,
      0,
      false,
      false,
      false,
      false,
      0,
      null
    );
    a.dispatchEvent(e);
  };
})(console);

var colToArr = (children) => {
  return Array.prototype.slice.call(children);
};

var array = colToArr(document.querySelector(".gwt-Tree").children);

var availables = {
  satliq: {
    isThere: false,
    keyword: "Density [L, G]",
    table: null,
  },
  satvap: {
    isThere: false,
    keyword: "Density [G, L]",
    table: null,
  },
  pvap: {
    isThere: false,
    keyword: "Phase boundary pressure",
    table: null,
  },
};

array.forEach((el) => {
  const innerText = el.innerText;
  if (innerText.includes("Phase boundary pressure")) {
    availables.pvap.isThere = true;
  } else if (innerText.includes("Density")) {
    if (el.children[1]) {
      const densities = colToArr(el.children[1].children);
      for (let i = 0; i < densities.length; i++) {
        const dEl = densities[i];
        if (dEl.innerText.includes("L, G")) {
          availables.satliq.isThere = true;
        } else if (dEl.innerText.includes("G, L")) {
          availables.satvap.isThere = true;
        }
      }
    } else {
      if (innerText.includes("L, G")) {
        availables.satliq.isThere = true;
      } else if (innerText.includes("G, L")) {
        availables.satvap.isThere = true;
      }
    }
  }
});

var windows = document.querySelectorAll(".wtt-BaseWindow");
windows.forEach((el) => {
  for (const p in availables) {
    const prop = availables[p];
    if (prop.isThere && el.innerText.includes(prop.keyword)) {
      const tbody = el
        .querySelector(".wtt-BaseWindowInterior")
        .querySelector("tbody");
      const trs = colToArr(tbody.children);
      let str = "";
      for (let i = 0; i < trs.length; i++) {
        const tds = colToArr(trs[i].children);
        for (let i = 0; i < tds.length; i++) {
          str += tds[i].innerText;
          if (i !== tds.length - 1) {
            str += ",";
          }
        }
        str += "\n";
      }
      availables[p].table = str;
    }
  }
});

availables.compound = compound;
console.save(availables, "jsonData.json");
