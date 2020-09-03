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

/********************/
/* GLOBAL VARIABLES */
/********************/

const cuisines = [
	'african',
	'chinese',
	'japanese',
	'korean',
	'vietnamese',
	'thai',
	'indian',
	'british',
	'irish',
	'french',
	'italian',
	'mexican',
	'spanish',
	'middle eastern',
	'jewish',
	'american',
	'cajun',
	'southern',
	'greek',
	'german',
	'nordic',
	'eastern european',
	'caribbean',
	'latin american'
];
const diets = [ 'pescetarian', 'lacto vegetarian', 'ovo vegetarian', 'vegan', 'vegetarian' ];
const sentinel = document.querySelector('#sentinel');
let offset;
const intersectionObserver = new IntersectionObserver((entries) => {
	if (entries[0].intersectionRatio <= 0) {
		return;
	}
	loadItems();
});

/*******************/
/* EVENT LISTENERS */
/*******************/

$('#add-ingredients').on('click', addIngredientsToGroceryList);
$('.remove').on('click', confirmRemove);
$('#send-email').on('click', sendEmail);
$('#clear-list').on('click', clearList);
$('.favorite-form').on('click', '.fa-heart', handleFavorite);
$('#update').on('click', showUpdateForm);
$('#search-form').on('submit', handleSearch);
$('#show-add-ingredient').on('click', showAddIngredient);
if (sentinel !== null) intersectionObserver.observe(sentinel);

/*****************/
/*	  ON LOAD	 */
/*****************/

$(document).ready(function() {
	// Flashed messages fade in and out
	$('#flash').hide().delay(300).fadeIn(500).delay(3000).fadeOut(800);

	// Reset offset to 0 unless you already have results
	offset = 0;
	if ($('#recipe-container').length) offset = 12;
});

/*****************/
/*	 	AJAX	 */
/*****************/

async function loadItems() {
	const id = $(this).data('id');
	const query = $('#search-value').val();
	const diet = $('#diet').val();
	const cuisine = $('#cuisine').val();

	const response = await axios.get('/load', { params: { id, query, diet, cuisine, offset } });

	if (response.data.data.results.length === 0) {
		$('#sentinel').html('No more recipes found!');
	} else {
		response.data.data.results.forEach((recipe) => {
			showRecipeCard(recipe, response.data.data, response.data.favorites);
		});

		$('.favorite-form').on('click', '.fa-heart', handleFavorite);
		offset += 12;
	}
}

async function handleSearch(evt) {
	evt.preventDefault();
	const id = $(this).data('id');
	const query = $('#search-value').val();
	const diet = $('#diet').val();
	const cuisine = $('#cuisine').val();
	offset = 0;

	const response = await axios.get('/search', { params: { id, query, diet, cuisine, offset } });
	if (response.status !== 200) {
		console.log('There was an error - please refresh and try again');
		console.log('response: ', response);
	} else {
		displayResults(response);
	}

	setTimeout(() => {
		if (!$('#sentinel').length) addSetinel();
		offset += 12;
	}, 800);
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
	const ingredient = $(this).closest('li').text();
	const response = await axios.patch(`/groceries/${listId}`, (data = { id, ingredient }));

	displayAndRemove.call(this, response.data);
}

async function sendEmail() {
	const id = $(this).data('id');
	response = await axios.get(`/email/${id}`);

	if (response.data.errors) {
		displayErrorAlert(response);
	} else {
		displaySuccessAlert(response);
	}
}

async function clearList() {
	const id = $(this).data('id');
	response = await axios.delete(`/groceries/${id}`);

	if (response.status !== 200) {
		displayErrorAlert(response);
	} else {
		updateListContainer();
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
	const response = await axios.patch(`/users/${id}`, (data = { id, email, imgUrl }));

	if (response.data.errors) {
		displayErrorAlert(response);
	} else {
		updateProfile(response);
		displaySuccessAlert(response);
	}
}

async function handleAddIngredient(evt) {
	evt.preventDefault();
	const id = $(this).closest('ul').data('id');
	const ingredient = $('#user-add-ingredient').val();

	const response = await axios.post(`/groceries/${id}`, (data = { ingredient }));

	if (response.status === 201) {
		const newItem = generateIngredientHTML(response.data.ingredient);
		$(this).closest('li').html(newItem);
	} else {
		const data = { message: `Couldn't add ${ingredient}. Refresh and try again` };
		displayAndRemove(data);
	}
}
