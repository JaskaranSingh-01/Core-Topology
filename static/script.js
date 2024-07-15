window.onload = function () {
    require.config({
        paths: {
            ipysigma: 'https://unpkg.com/ipysigma@0.24.2/dist/ipysigma'
        }
    });
    require(['@jupyter-widgets/html-manager'], function (htmlManager) {
        const widgetState = JSON.parse(document.getElementById('widget-state').textContent);
        const manager = new htmlManager.HTMLManager();
        manager.set_state(widgetState).then(models => {
            for (let model_id in models) {
                const model = models[model_id];
                const view = manager.create_view(model);
                view.then(view_instance => {
                    document.getElementById('widget-container').appendChild(view_instance.el);
                    manager.display_view(view_instance);
                });
            }
        });
    });




};


window.onchange = function () {
    var e = document.getElementsByClassName('ipysigma-information-contents')
    var node = e.item(0).getElementsByTagName('i')[0].innerText
    $.ajax({
        url: '/form1/process',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'value': node }),
        success: function (response) {
            console.log("Data successfully sent:", response);
        },
        error: function (error) {
            console.log("Error:", error);
        }
    });

    // Add confirmation prompt before opening the new link
    var userConfirmed = confirm("Do you want to open the next link?");
    if (userConfirmed) {
        // $.ajax({
        //     url: '/process',
        //     type: 'POST',
        //     contentType: 'application/json',
        //     data: JSON.stringify({ 'value': node }),


        //     error: function (error) {
        //         console.log(error);
        //     }
        // });
        // Alternatively, you can use: window.location.href = "/ugandabasic/process";
        window.open("/form1/process");
    }


    // window.open("/ugandabasic/process")
    // window.location.href = "/ugandabasic/process"
    var node = e.item(0).getElementsByTagName('i')[0].innerText
    console.log(node)
};

document.addEventListener('DOMContentLoaded', (event) => {
    // Create a new button element
    const button = document.createElement('button');
    button.innerText = 'Download .html file';
    button.classList.add('ipysigma-button');
    button.style.margin = '3px';
    button.style.padding = '1rem';

    // Get the first element with the specified class name
    var item = document.querySelector('.ipysigma-download-controls');
    
    // Add an event listener to the button
    button.addEventListener('click', () => {
        window.location.href = '/generate_html';
    });
    
    if (document.body && document.body.lastChild.innerText != 'Download .html file') {
        document.body.appendChild(button);
    }
});

async function fetchScriptContent(url) {
    const response = await fetch(url);
    return await response.text();
}