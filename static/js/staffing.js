document.addEventListener("DOMContentLoaded", function () {

    console.log("✅ staffing.js loaded");

    let maxWorkers = parseInt(document.getElementById("maxWorkers").value);

    /* Slider values */
    function syncSlider(id) {
        document.getElementById(id + "Value").textContent =
            document.getElementById(id).value;
    }

    ["openingHour", "closingHour", "maxWorkers"].forEach(id => {
        syncSlider(id);
        document.getElementById(id).addEventListener("input", () => {
            syncSlider(id);
            if (id === "maxWorkers") {
                maxWorkers = parseInt(document.getElementById(id).value);
            }
        });
    });

    /* Cell coloring */
    function updateCellColor(cell, workers) {
        [...cell.classList].forEach(c => {
            if (c.startsWith("workers-")) cell.classList.remove(c);
        });
        cell.classList.add("workers-" + Math.min(workers, 5));
    }

    /* Cell click */
    document.querySelectorAll(".open-hour").forEach(cell => {
        cell.addEventListener("click", () => {
            let workers = parseInt(cell.dataset.workers);
            workers = workers % maxWorkers + 1;
            cell.dataset.workers = workers;
            cell.textContent = workers;
            updateCellColor(cell, workers);
        });
    });

    /* +1 per hour */
    document.querySelectorAll(".hour-plus-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const hour = btn.dataset.hour;
            document.querySelectorAll(`.open-hour[data-hour="${hour}"]`)
                .forEach(cell => {
                    let workers = parseInt(cell.dataset.workers);
                    workers = workers % maxWorkers + 1;
                    cell.dataset.workers = workers;
                    cell.textContent = workers;
                    updateCellColor(cell, workers);
                });
        });
    });

    /* Save */
    window.saveConfig = function () {

        const cells = [];
        document.querySelectorAll(".open-hour").forEach(cell => {
            cells.push({
                day: parseInt(cell.dataset.day),
                hour: parseInt(cell.dataset.hour),
                workers: parseInt(cell.dataset.workers)
            });
        });

        const closedDays = [];
        document.querySelectorAll(".closed-day-checkbox:checked")
            .forEach(cb => closedDays.push(parseInt(cb.value)));

        fetch("", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                opening_hour: parseInt(document.getElementById("openingHour").value),
                closing_hour: parseInt(document.getElementById("closingHour").value),
                max_workers: parseInt(document.getElementById("maxWorkers").value),
                closed_days: closedDays,
                cells: cells
            })
        }).then(() => alert("Configuration saved"));
    };

});
