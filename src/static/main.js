const chart = document.getElementById("thermals-chart");
const print_info_body = document.getElementById("print-info-body");

function set_spinner(progress) {
    const spinner_text = document.getElementById("progress-spinner-text");
    const spinner_svg = document.getElementById("progress-spinner-overlay");

    progress = Math.round(progress * 100);

    if (progress >= 100) {
        progress = 100;
    }

    spinner_text.textContent = `${progress}%`;
    spinner_svg.setAttribute("stroke-dashoffset", progress);
}

function init_chart() {
    new Chart(chart, {
        type: 'bar',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function request_update() {
    let request = new XMLHttpRequest();

    try {
        request.open("GET", "api/update")

        request.responseType = "json";

        request.addEventListener("load", () => process_update(request.response));
        request.addEventListener("error", () => {
            // console.error(`Request error ${request.status}: ${request.error}`)
            set_error("Printer offline")
        });

        request.send();
    } catch (error) {
        console.error(`Request error ${request.status}: ${error}`);
    }
}

function set_icon(filename) {
    let thumb = document.getElementById("print_thumb");
    let path = filename.split("/");
    let gcode = path.pop();

    path.push(`.thumbs/${gcode.substring(0, gcode.search(".gcode"))}-400x300.png`);

    try {
        thumb.src = `http://voron24.hacklab/server/files/gcodes/${path.join("/")}`;
    } catch (error) {

    }
}

function set_print_info(path, state) {
    let body = document.getElementById("print-info-body");
    let children = body.children;
    children.item(0).textContent = `File: ${path.substring(0, path.search(".gcode"))}`;
    children.item(1).textContent = `State: ${state}`;
}

function set_error(msg) {
    let widget = document.getElementById("error-text");
    document.getElementsByClassName("print-info")[0].style.display = "none";
    widget.textContent = msg;
    widget.parentElement.parentElement.style.display = "block";
}

function unset_error() {
    let widget = document.getElementById("error-text");
    widget.parentElement.parentElement.style.display = "none";
    document.getElementsByClassName("print-info")[0].style.display = "block";

}

async function process_update(response) {
    // console.table(response);

    switch (response.printer_state) {
        case "standby":
            set_print_info("", "Ready");
            break;
        case "complete":
        case "printing":
        case "paused":
        case "cancelled":
            unset_error();
            set_spinner(response.file_info.progress);
            set_print_info(response.file_info.path, response.printer_state);
            set_icon(response.file_info.path);
            break;
        case "error":
            set_error(response.message);
            break;
    }
}

// init_chart();
// Set spinner to 0% initially
set_spinner(0);

request_update();
// Update once every 30 seconds. Since printers operate over hours, the data won't change frequently
setInterval(request_update, 30 * 1000);
