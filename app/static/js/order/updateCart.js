let changedInputs = new Set();

function stepDown(button, itemId) {
    const $inputElement = $(button).parent().find('input[type=number]');
    $inputElement[0].stepDown();
    changedInputs.add(itemId);
}

function stepUp(button, itemId) {
    const $inputElement = $(button).parent().find('input[type=number]');
    $inputElement[0].stepUp();
    changedInputs.add(itemId);
}

function changeQuantity(itemId) {
    changedInputs.add(itemId);
}

function saveClick() {
    if (changedInputs.size === 0) {
        console.log('No changes to save.');
        return;
    }

    const data = [];
    changedInputs.forEach(itemId => {
        const $inputElement = $('#' + itemId);
        if ($inputElement.length) {
            data.push({
                id: itemId,
                quantity: $inputElement.val()
            });
        } else {
            console.error(`Input element with ID ${itemId} not found.`);
        }
    });

    if (data.length === 0) {
        console.log('No valid input elements found.');
        return;
    }

    const url = $('meta[name="update-cart"]').attr('content');
    const csrfToken = $('meta[name="csrf-token"]').attr('content');

    $.ajax({
        url: url,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(result) {
            console.log('Update successful:', result);
            changedInputs.clear();
            if (result.success) {
                location.reload();
            } else {
                console.error('Failed to update cart:', result.message);
            }
        },
        error: function(error) {
            console.error('Error updating cart:', error);
        }
    });
}

function deleteClick(itemId) {
    const url = $('meta[name="update-cart"]').attr('content');
    const csrfToken = $('meta[name="csrf-token"]').attr('content');

    $.ajax({
        url: url,
        type: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        },
        contentType: 'application/json',
        data: JSON.stringify({ id: itemId }),
        success: function(result) {
            console.log('Delete successful:', result);
            if (result.success) {
                location.reload();
            } else {
                console.error('Failed to delete item:', result.message);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error deleting item:', error);
        }
    });
}
