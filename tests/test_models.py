from api.main import ProductModel
import pytest 


@pytest.fixture() 
def mock_product(): 
	return ProductModel(
		title = "abc",
		description = "abc",
		ean = "123",
		upc = "abc",
		brand = "Starbucks",
		model = "abc",
		category = "abc > def > ghi",
		image_url = "abc",
	)


def test_product_categories(mock_product): 
	assert mock_product.get_precise_category() == "ghi"

def test_product_categories_no_nesting(mock_product): 
	mock_product.category = "abc"
	assert mock_product.get_precise_category() == "abc"

