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
    node.addEventListener('mouseover',(event)=>{
        node.style.fontSize= "16px" ;
        node.style.cursor= "pointer" ;
    })
    node.addEventListener('mouseout',(event)=>{
        node.style.fontSize= "12px" ;
        node.style.cursor= "default" ;
    })
    node.addEventListener('click', (event) => {
        console.log(node)
        fetch('/get_data/' + node.innerText)
            .then(response => response.json())
            .then(data => {
                console.log(data)

                let popup = document.getElementById('popup');
                popup.innerHTML = '';
                data.forEach(item => {
                    let d = document.createElement('div')
                    for (const [key, value] of Object.entries(item)) {
                        let p = document.createElement('p');
                        p.textContent = `${key}: ${value}`;
                        d.appendChild(p);
                    }
                    popup.appendChild(d);
                    popup.appendChild(document.createElement('hr')); // Add a horizontal rule for separation
                });
                popup.style.display = 'block';
                popup.style.position = 'absolute'
                popup.style.top = '4rem' 
                popup.style.width = '50%';
                popup.style.height= '40vh';
                popup.style.background= '#212121';
                popup.style.color= 'white';
                popup.style.borderRadius= '1rem';
                popup.style.padding= '3rem';
                popup.style.overflow= 'auto';

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
