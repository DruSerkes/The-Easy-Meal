/* 
// ANIMATIONS
*/
$(document).ready(function() {
	// Flashed messages fade in and out
	$('#flash').hide().delay(300).fadeIn(500).delay(3000).fadeOut(800);
	// Enable Tooltips
	$('[data-toggle="tooltip"]').tooltip();
});

/* 
// AJAX
*/

//
$('#add-ingredients').on('click', addIngredientsToGroceryList);

async function addIngredientsToGroceryList(evt) {
	const id = $(this).data('id');
	response = await axios.post(`/groceries`, (data = { id }));
	const modalHTML = generateModalHTML(response.data);
	$('body > .container').append(modalHTML);
	$('#myModal').modal('show');
}

$('#remove').on('click', changeToConfirmRemove);

async function removeIngredientFromGroceryList(evt) {
	const id = $(this).data('id');
	const listId = $(this).closest('ul').attr('id');
	const response = await axios.patch(`/groceries/${listId}`, (data = { id }));

	displayAndRemove.call(this, response.data);
}

// TODO send an email 



// TODO Remove all items from list

/* 
// HELPERS
*/

function displayAndRemove(data) {
	console.log(this);
	const $toRemove = $(this).closest('li');
	$toRemove.html(`${data.message}`);
	$toRemove.delay(500).fadeOut(2000);
}

function changeToConfirmRemove() {
	$(this).removeClass('far fa-trash-alt');
	$(this).addClass('fas fa-minus-circle');
	$(this)
		.attr('id', 'confirm-remove')
		.attr('data-toggle', 'tooltip')
		.attr('data-placement', 'right')
		.attr('title', 'Remove from list')
		.tooltip()
		.on('click', removeIngredientFromGroceryList);
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

function generateAlertHTML(data) {
	// return html for an alert
	return `<div class="alert alert-success" role="alert">
	Ingredient removed from list.
  </div>`;
}
