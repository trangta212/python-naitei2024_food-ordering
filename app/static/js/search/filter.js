document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const categorySelect = document.getElementById('category-select');
    const priceOrderSelect = document.getElementById('price-order-select');

    function updateURL() {
        const form = document.getElementById('filter-form');
        const url = new URL(window.location.href);
        
        // Update URL with search query
        url.searchParams.set('q', searchInput ? searchInput.value : '');
        
        // Update URL with category and price order
        if (categorySelect) {
            url.searchParams.set('category', categorySelect.value);
        }
        if (priceOrderSelect) {
            url.searchParams.set('price_order', priceOrderSelect.value);
        }

        // Reload the page with updated URL
        window.location.href = url.toString();
    }

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // Debounce to limit the rate of URL updates
            clearTimeout(searchInput.timeout);
            searchInput.timeout = setTimeout(updateURL, 300); // 300ms debounce
        });
    }

    if (categorySelect) {
        categorySelect.addEventListener('change', updateURL);
    }

    if (priceOrderSelect) {
        priceOrderSelect.addEventListener('change', updateURL);
    }
});
