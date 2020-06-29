/* 
// ANIMATIONS
*/

$(document).ready(function() {
	// Flashed messages fade in and out
	$('#flash').hide().delay(300).fadeIn(500).delay(3000).fadeOut(800);
	// Enable Tooltips
	// $('[data-toggle="tooltip"]').tooltip();
});

/* 
// LISTENERS
*/

$('#add-ingredients').on('click', addIngredientsToGroceryList);
$('#remove').on('click', confirmRemove);
$('#send-email').on('click', sendEmail);
$('#clear-list').on('click', clearList);
$('#favorite-form').on('click', '.fa-heart', handleFavorite);

/* 
// AJAX
*/

async function addIngredientsToGroceryList(evt) {
	const id = $(this).data('id');
	response = await axios.post(`/groceries`, (data = { id }));
	const modalHTML = generateGroceryModalHTML(response.data);
	$('body > .container').append(modalHTML);
	$('#myModal').modal('show');
}

async function removeIngredientFromGroceryList(evt) {
	const id = $(this).data('id');
	const listId = $(this).closest('ul').data('id');
	const response = await axios.patch(`/groceries/${listId}`, (data = { id }));

	displayAndRemove.call(this, response.data);
}

async function sendEmail() {
	const id = $(this).data('id');
	response = await axios.get(`/email/${id}`);

	if (response.data.errors) {
		const alertHTML = generateAlertHTML(response.data.errors, 'danger');
		$('body').append(alertHTML).alert();
		$('.feedback').hide().fadeIn(1500).delay(500).fadeOut(2000);
	} else {
		const alertHTML = generateAlertHTML(response.data.message, 'success');
		$('body').append(alertHTML).alert();
		$('.feedback').hide().fadeIn(1500).delay(500).fadeOut(2000);
	}
}

async function clearList() {
	const id = $(this).data('id');
	response = await axios.delete(`/groceries/${id}`);

	if (response.status !== 200) {
		const alertHTML = generateAlertHTML(response.data.errors, 'danger');
		$('body').append(alertHTML).alert();
		$('.feedback').hide().fadeIn(1500).delay(500).fadeOut(2000);
	} else {
		const alertHTML = generateAlertHTML(response.data.message, 'success');
		$('body').append(alertHTML).alert();
		$('.feedback').hide().fadeIn(1500).delay(1000).fadeOut(2200);
		$('#list').empty();
	}
}

async function handleFavorite(evt) {
	evt.preventDefault();
	const id = $(this).closest('button').data('id');

	if ($(this).hasClass('fas')) {
		let response = await axios.delete(`/favorites/${id}`);
		toggleFavorite.call(this, response);
	} else {
		let response = await axios.post(`/favorites/${id}`, (data = { id }));
		toggleFavorite.call(this, response);
	}
}

/* 
// HELPERS
*/

function toggleFavorite(response) {
	if (response.status !== 200) {
		displayError(response);
	} else {
		$(this).toggleClass('fas fa-heart');
		$(this).toggleClass('far fa-heart');
		displaySuccess(response);
	}
}

function displayError(response) {
	const alertHTML = generateAlertHTML(response.data.errors, 'danger');
	$('body').append(alertHTML).alert();
	$('.feedback').hide().fadeIn(1500).delay(500).fadeOut(2000);
}

function displaySuccess(response) {
	const modalHTML = generateRecipeModalHTML(response.data);
	if ($('#myModal')) {
		$('#myModal').remove();
	}
	$('body > .container').append(modalHTML);
	$('#myModal').modal('show');
}

function displayAndRemove(data) {
	const $toRemove = $(this).closest('li');
	$toRemove.html(`${data.message}`);
	$toRemove.delay(500).fadeOut(2000);
}

function confirmRemove() {
	$(this).removeClass('far fa-trash-alt');
	$(this).addClass('fas fa-minus-circle');
	$(this)
		.attr('id', 'confirm-remove')
		.attr('data-toggle', 'tooltip')
		.attr('data-placement', 'right')
		.attr('title', 'Remove from list')
		.tooltip()
		.on('click', removeIngredientFromGroceryList)
		.tooltip('hide');
}

function generateGroceryModalHTML(data) {
	return `<div id="myModal" class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
	<div class="modal-content">
	  <div class="modal-header">
		<p class="mx-auto my-0">${data.message}</p>
      </div>
	  <div class="modal-footer">
        <a class="btn btn-primary text-white ml-auto" href="/groceries/${data.grocery_list
			.id}") }}">Go to Shopping List</a>
        <button type="button" class="btn btn-secondary mr-auto" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>`;
}

function generateRecipeModalHTML(data) {
	return `<div id="myModal" class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
	<div class="modal-content">
	  <div class="modal-header">
		<p class="mx-auto my-0">${data.message}</p>
      </div>
	  <div class="modal-footer">
        <a class="btn btn-primary text-white ml-auto" href="/recipes/${data.recipe.id}") }}">Recipe Details</a>
        <button type="button" class="btn btn-secondary mr-auto" data-dismiss="modal">Thanks</button>
      </div>
    </div>
  </div>
</div>`;
}

function generateAlertHTML(message, category) {
	return `<div class="container w-75 mx-auto feedback">
	<div class="alert alert-${category} alert-dismissible fade show text-center" role="alert">
	${message}
	<button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
  </div>
  </div>`;
}
