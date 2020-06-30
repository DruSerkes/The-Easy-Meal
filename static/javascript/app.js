/* TODO MAYBE WISE TO REFACTOR INTO OOP
0. Create api-classes.js and include in base.html before ui.js 
1. Create User class
2. User attributes: id, email, favorite recipes, diet, cuisine, (intolerances?)
3. Move appropriate methods onto user (handleSearch, sendEmail, etc)
4. Repeat for GroceryList class...
5. GroceryList attributes: id, ingredients,
6. Repeat for Recipe class... 
7. Recipe attributes: id, title, imgUrl, sourceName, sourceUrl, description, readyIn, servings, ingredients(list) 
*/

/* 
// ANIMATION ON LOAD 
*/

$(document).ready(function() {
	// Flashed messages fade in and out
	$('#flash').hide().delay(300).fadeIn(500).delay(3000).fadeOut(800);
	// Enable Tooltips
	// $('[data-toggle="tooltip"]').tooltip();
});

/* 
// EVENT LISTENERS
*/

$('#add-ingredients').on('click', addIngredientsToGroceryList);
$('#remove').on('click', confirmRemove);
$('#send-email').on('click', sendEmail);
$('#clear-list').on('click', clearList);
$('#favorite-form').on('click', '.fa-heart', handleFavorite);
$('#update').on('click', showUpdateForm);
$('#search-form').on('submit', handleSearch);
/* 
// AJAX
*/

async function handleSearch(evt) {
	evt.preventDefault();
	const id = $(this).data('id');
	const query = $('#search-value').val();
	if (query === '') {
		doNothingOnSubmit();
	}

	const response = await axios.get('/search', { params: { query, id } });
	displayResults(response);
}

function displayResults(response) {
	$('main').children().fadeOut(500).remove();
	setTimeout(() => {
		const $h1 = makeH1();
		const $row = makeRow();
		$('main').append($h1).fadeIn(500);
		$('h1').after($row);
		response.data.results.forEach((recipe) => {
			showRecipeCard(recipe, response.data);
		});
	}, 500);
}

function showRecipeCard(recipe, data) {
	const recipeHTML = generateRecipeCardHTML(recipe, data);
	$('#recipe-container').append(recipeHTML).hide().fadeIn(500);
}

// TODO JINJA elements need attention
function generateRecipeCardHTML(recipe, data) {
	return `<div class="card col-sm-10 col-md-5 col-lg-4 col-xl-3 border border-secondary p-2 rounded text-center my-3">
	<img src="${data.baseUri}${recipe.image}" class="card-img-top img-fluid" alt="Photo of ${recipe.title}">
	<div class="card-body py-2">
	  <h5 class="card-title d-inline">${recipe.title}</h5>
	  <form id="favorite-form" class="d-inline">
		{% if recipe in g.user.recipes %}
		<button data-id="${recipe.id}" class='btn btn-sm'><span><i  class="fas fa-heart"></i></span></button>
		{% else %}
		<button data-id="${recipe.id}" class='btn btn-sm'><span><i class="far fa-heart"></i></span></button>
		{% endif %}
	  </form>
	  <p class="lead mb-0">Ready In: ${recipe.readyInMinutes}</p>
	  <p class="lead">Servings: ${recipe.servings}</p>
	  <a class="small text-muted" href="${recipe.sourceUrl}">View original</a>
	  <br>
	  <a href="{{ url_for('view_recipe_details', id=recipe.id) }}" class="btn btn-outline-primary">See more</a>
	</div>
</div>`;
}

function makeH1(text = 'Easy Meals') {
	let $newH1 = $('<h1>').text(text).addClass('display-2 text-center');
	return $newH1;
}
function makeRow() {
	let $newRow = $('<div>').addClass('row p-0 m-0').attr('id', 'recipe-container');
	return $newRow;
}

async function addIngredientsToGroceryList(evt) {
	const id = $(this).data('id');
	response = await axios.post(`/groceries`, (data = { id }));
	const modalHTML = generateGroceryModalHTML(response.data);
	addShowModal(modalHTML);
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
		displayErrorAlert(response);
	} else {
		displaySuccessAlert(response);
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

async function handleUserUpdate(evt) {
	evt.preventDefault();

	const id = $(this).data('id');
	const email = $('#email').val();
	const imgUrl = $('#img-url').val();
	let response = await axios.patch(`/users/${id}`, (data = { id, email, imgUrl }));

	if (response.data.errors) {
		displayErrorAlert(response);
	} else {
		updateProfile(response);
		displaySuccessAlert(response);
	}
}

/* 
// HELPERS
*/

function showUpdateForm() {
	const id = $(this).data('id');
	const modalHTML = generateUpdateModalHTML(id);
	addShowModal(modalHTML);
	$('#submit-update').on('click', handleUserUpdate);
}

function updateProfile(response) {
	$('#user-email').text(`Email: ${response.data.user.email}`);
	$('#user-image').attr('src', `${response.data.user.img_url}`);
	$('#user-profile').attr('src', `${response.data.user.img_url}`);
}

function toggleFavorite(response) {
	if (response.status !== 200) {
		displayErrorAlert(response);
	} else {
		$(this).toggleClass('fas fa-heart');
		$(this).toggleClass('far fa-heart');
		displaySuccessModal(response);
	}
}

function displayErrorAlert(response) {
	console.log(`Error details: ${response.data.errors}`);
	const alertHTML = generateAlertHTML('Something went wrong, please try again', 'danger');
	$('body').append(alertHTML).alert();
	$('.feedback').hide().fadeIn(1500).delay(500).fadeOut(3000);
}

function displaySuccessAlert(response) {
	const alertHTML = generateAlertHTML(response.data.message, 'success');
	$('main').append(alertHTML).alert();
	$('.feedback').hide().fadeIn(1500).delay(500).fadeOut(3000);
}

function displaySuccessModal(response) {
	const modalHTML = generateRecipeModalHTML(response.data);
	if ($('#myModal')) {
		$('#myModal').remove();
	}
	addShowModal(modalHTML);
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
        <a class="btn btn-primary text-white ml-auto" href="/groceries") }}">Go to Shopping List</a>
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

function addShowModal(modalHTML) {
	$('body > .container').append(modalHTML);
	$('#myModal').modal('show');
}

function doNothingOnSubmit(evt) {
	evt.preventDefault();
	return;
}

function generateUpdateModalHTML(id) {
	return `<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModal" aria-hidden="true">
	<div class="modal-dialog" role="document">
	  <div class="modal-content">
		<div class="modal-header">
		  <h5 class="modal-title text-center">Update Profile</h5>
		  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
			<span aria-hidden="true">&times;</span>
		  </button>
		</div>
		<div class="modal-body">
		  <form id="user-update">
			<div class="form-group">
			  <label for="email" class="col-form-label">Email:</label>
			  <input type="text" class="form-control" id="email">
			</div>
			<div class="form-group">
			  <label for="img-url" class="col-form-label">Image URL:</label>
			  <input type="url" class="form-control" id="img-url">
			</div>
		  </form>
		</div>
		<div class="modal-footer">
		  <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
		  <button data-id="${id}" data-dismiss="modal" id="submit-update" type="button" class="btn btn-primary">Update</button>
		</div>
	  </div>
	</div>
  </div>`;
}
