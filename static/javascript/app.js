/* 
// ANIMATIONS
*/
$(document).ready(function() {
	// Flashed messages fade in and out
	$('#flash').hide().delay(300).fadeIn(500).delay(3000).fadeOut(800);
	// Enable Tooltips
	$(function() {
		$('[data-toggle="tooltip"]').tooltip();
	});
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

async function removeIngredientFromGroceryList(evt) {
	const id = $(this).data('id');
	response = await axios.delete('/groceries', (data = { id }));
	// have DELETE /groceries remove ingredient with this id from the grocerylist
	// remove parent li
	// display alert
	// alert fades out after 2-3 seconds
	const alertHTML = generateAlertHTML(response.data);
}

/* 
// HELPERS
*/

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
