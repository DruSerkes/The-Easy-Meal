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

/* 
// AJAX
*/

async function addIngredientsToGroceryList(evt) {
	const id = $(this).data('id');
	response = await axios.post(`/groceries`, (data = { id }));
	const modalHTML = generateModalHTML(response.data);
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
		$('h1').after(alertHTML).alert();
	} else {
		const alertHTML = generateAlertHTML(response.data.message, 'success');
		$('h1').after(alertHTML).alert();
	}
}

async function clearList() {
	const id = $(this).data('id');
	response = await axios.delete(`/groceries/${id}`);

	if (response.status !== 200) {
		const alertHTML = generateAlertHTML(response.data.errors, 'danger');
		$('h1').after(alertHTML).alert().delay(300).fadeOut(3000);
	} else {
		const alertHTML = generateAlertHTML(response.data.message, 'success');
		$('h1').after(alertHTML).alert().delay(300).fadeOut(3000);
		$('#list').empty();
	}
}

async function addFavorite() {
	$('#')
}

/* 
// HELPERS
*/

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

function generateModalHTML(data) {
	return `<div id="myModal" class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">${data.message}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>${data.message}</p>
      </div>
      <div class="modal-footer">
        <a class="btn btn-primary text-white" href="/groceries/${data.grocery_list.id}") }}">Go to Shopping List</a>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>`;
}

function generateAlertHTML(message, category) {
	// return html for an alert
	return `<div class="container w-75 mx-auto">
	<div class="alert alert-${category} alert-dismissible fade show text-center" role="alert">
	${message}
	<button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
  </div>
  </div>`;
}
