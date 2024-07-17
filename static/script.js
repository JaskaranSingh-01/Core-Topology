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
    var node = e.item(0).getElementsByTagName('i')[0]
    node.addEventListener('mouseover', (event) => {
        node.style.fontSize = "16px";
        node.style.cursor = "pointer";
    })
    node.addEventListener('mouseout', (event) => {
        node.style.fontSize = "12px";
        node.style.cursor = "default";
    })
    node.addEventListener('click', (event) => {
        console.log(node)
        fetch('/get_data/' + node.innerText)
            .then(response => response.json())
            .then(data => {
                console.log(data)

                let popup = document.getElementById('popup');
                popup.innerHTML = ''; // Clear previous content

                // Create a table
                let table = document.createElement('table');

                // Create table header
                let thead = document.createElement('thead');
                let headerRow = document.createElement('tr');
                if (data.length > 0) {
                    Object.keys(data[0]).forEach(key => {
                        let th = document.createElement('th');
                        th.textContent = key;
                        th.style.border = '1px solid white';
                        th.style.padding = '10px';
                        th.style.textAlign = 'left';
                        headerRow.appendChild(th);
                    });
                }
                thead.appendChild(headerRow);
                table.appendChild(thead);

                // Create table body
                let tbody = document.createElement('tbody');
                data.forEach(item => {
                    let row = document.createElement('tr');
                    Object.values(item).forEach(value => {
                        let td = document.createElement('td');
                        td.textContent = value;
                        td.style.border = '1px solid white';
                        td.style.padding = '10px';
                        td.style.textAlign = 'left';
                        row.appendChild(td);
                    });
                    tbody.appendChild(row);
                });
                table.appendChild(tbody);
                table.style.width = '100%';
                table.style.borderCollapse = 'collapse';
                table.style.borderCollapse = '1px solid white';
                table.style.borderRadius = '1.5rem';
                popup.appendChild(table);
                popup.style.display = 'block';
                popup.style.position = 'absolute'
                popup.style.top = '2rem'
                popup.style.width = 'fit-content';
                popup.style.height = '40vh';
                popup.style.background = '#212121';
                popup.style.color = 'white';
                popup.style.borderRadius = '1rem';
                popup.style.padding = '3rem';
                popup.style.overflow = 'auto';
                popup.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.5)'

            })
            .catch(error => console.error('Error:', error));
    })


    // var node = e.item(0).getElementsByTagName('i')[0].innerText
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


window.onclick = function (event) {
    let popup = document.getElementById('popup');
    if (event.target !== popup && !popup.contains(event.target)) {
        popup.style.display = 'none';
    }
};
