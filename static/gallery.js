document.addEventListener('DOMContentLoaded', function() {
    const galleryContainer = document.querySelector('.gallery-container');
    const jsonUrl = galleryContainer.getAttribute('data-json-url');

    fetch(jsonUrl)
        .then(response => response.json())
        .then(data => {
            const gallery = document.getElementById('gallery');
            data.forEach((item, index) => {
                const galleryItem = document.createElement('div');
                galleryItem.className = 'gallery-item';

                const img = document.createElement('img');
                img.src = item.image;
                img.alt = item.name;
                img.dataset.index = index;

                const info = document.createElement('div');
                info.className = 'gallery-item-info';

                const title = document.createElement('h3');
                title.textContent = item.name;

                const description = document.createElement('p');
                description.textContent = item.description;

                info.appendChild(title);
                info.appendChild(description);
                galleryItem.appendChild(img);
                galleryItem.appendChild(info);
                gallery.appendChild(galleryItem);

                img.addEventListener('click', () => {
                    localStorage.setItem('selectedItem', JSON.stringify(item));
                    window.location.href = '/gallery_view';
                });
            });
        })
        .catch(error => console.error('Error loading gallery data:', error));
});
