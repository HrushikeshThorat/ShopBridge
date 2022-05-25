from math import prod
import sys
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ShopBridge.models import ProductInventory
from .exceptions import InvalidInputException, WrongInputException


class InventoryProduct(viewsets.ViewSet):
        
    def create(self, request):
        '''
        Function will add new product in inventory 
      
        Parameters:
        name        (string)    : Name of product
        description (string)    : Description of product
        price       (float)     : Price of product
        quantity    (int)       : Quantity of product
    
        Returns:
        Response    (dict)      : Contains new Product_Id, Name and Message 
        '''
        dic = {}
        try:
            print('In create')
            name = request.data['name']
            description = request.data['description']
            price = request.data['price']
            quantity = request.data['quantity']
            
            # Check whether value is empty or not
            if (not name or not description or not price or not quantity):
                raise InvalidInputException
            else:
                try:
                    price = float(price)
                    quantity = int(quantity)
                except:
                    raise InvalidInputException

            # Add entry in database            
            newProduct = ProductInventory.objects.create(name = name, description = description, 
                                                  price = price, quantity = quantity)
            print('Product added successfully.')
            dic['data'] = {'product_Id': newProduct.product_Id, 'name': newProduct.name}
            dic['message'] = 'Product added successfully.'
        except InvalidInputException as e:
            print('In Viewset_Inventory => create', e.description)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = e.description
        except Exception as e:
            print('In Viewset_Inventory => create', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = '''Product can't be added.'''
        dic['status'] = 200
        return Response(data=dic)
            
    def retrieve(self, request, pk):
        '''
        Function will retrieve product details in inventory 
      
        Parameters:
        Product Id  (int)   : Product_Id of product 
    
        Returns:
        Response    (dict)  : Contains Product details (Id, name, description, quantity and 
                              price) and Message 
        '''
        dic = {}
        try:
            print('In retrieve')
            # Check whether Product_Id is valid or not
            try:
                pk = int(pk)
            except:
                raise InvalidInputException

            # Retrieve product details from database
            productDetails = list(ProductInventory.objects.filter(product_Id = pk).values())
            
            # Check whether given product_Id is exists or not
            if len(productDetails) == 0:
                raise WrongInputException
            print('Product details retrieve successfully.')
            dic['data'] = productDetails
            dic['message'] = 'Product details retrieve successfully.'
        except (InvalidInputException, WrongInputException) as e:
            print('In Viewset_Inventory => retrieve', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = e.description
        except Exception as e:
            print('In Viewset_Inventory => retrieve', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = '''Product details can't be retrieved.'''
        dic['status'] = 200
        return Response(data=dic)
    
    @action(methods=['post'], detail=False)
    def listProducts(self, request):
        '''
        Function will retrieve all product details in inventory 
      
        Parameters:
        SearchKey   (string): Product Name or empty for all
        page        (dict)  : Contains Page Size and Page Number
    
        Returns:
        Response    (dict)  : Contains All Product details (Id, name, description, quantity and 
                              price) and Message 
        '''
        dic = {}
        try:
            print('In listProducts')
            searchKey = request.data['searchKey'] if "searchKey" in request.data else ""
            pageDict = request.data['page'] if "page" in request.data else dict()
            
            # Retrieve product list from database
            if searchKey:
                productList = ProductInventory.objects.filter(name = searchKey).values()
            else:
                productList = ProductInventory.objects.values()

            # Check whether given product_ is exists or not
            if len(productList) == 0:
                message = 'No product exists in inventory.'
            else:
                # Applying sorting based on product_Id
                productList = sorted(productList, key=lambda d: d['product_Id'])
                
                # Applyig pagination
                if pageDict:
                    try:
                        pageSize = int(pageDict['pageSize'])
                        pageNumber = int(pageDict['pageNumber'])
                    except:
                        raise InvalidInputException

                    # All product list will display
                    if pageNumber == 0: 
                        pass
                    else:
                        startIndex = (pageNumber - 1) * pageSize
                        endIndex = pageNumber * pageSize
                        productList = productList[startIndex:endIndex]
                message = 'Product list retrieve successfully.'
            print('Product list retrieve successfully.')
            dic['data'] = productList
            dic['message'] = message
        except (InvalidInputException, WrongInputException) as e:
            print('In Viewset_Inventory => update', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = e.description
        except Exception as e:
            print('In Viewset_Inventory => listProducts', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = '''Product list can't be retrieved.'''
        dic['status'] = 200
        return Response(data=dic)
    
    def update(self, request, pk):
        '''
        Function will update existing product in inventory 
      
        Parameters:
        pk          (int)       : Product_Id
        name        (string)    : Name of product
        description (string)    : Description of product
        price       (float)     : Price of product
        quantity    (int)       : Quantity of product
    
        Returns:
        Response    (dict)      : Contains Product_Id, Name and Message 
        '''
        dic = {}
        try:
            print('In update')
            # Check whether Product_Id is valid or not
            try:
                pk = int(pk)
            except:
                raise InvalidInputException

            name = request.data['name']
            description = request.data['description']
            price = request.data['price']
            quantity = request.data['quantity']
                        
            # Check whether value is empty or not
            if (not name or not description or not price or not quantity):
                raise InvalidInputException
            else:
                try:
                    price = float(price)
                    quantity = int(quantity)
                except:
                    raise InvalidInputException

            # Update product details from database
            productUpdateStatus = ProductInventory.objects.filter(product_Id = pk).update(name = name,
                            description = description, price = price, quantity = quantity)
            
            # Check whether given product_Id is exists or not
            if productUpdateStatus == 0:
                raise WrongInputException

            print('Product details updated successfully.')
            dic['data'] = {'product_Id': pk, 'name': name}
            dic['message'] = 'Product details updated successfully.'
        except (InvalidInputException, WrongInputException) as e:
            print('In Viewset_Inventory => update', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = e.description
        except Exception as e:
            print('In Viewset_Inventory => update', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = '''Product details can't be updated.'''
        dic['status'] = 200
        return Response(data=dic)
    
    def delete(self, request, pk):        
        '''
        Function will delete product in inventory 
      
        Parameters:
        Product Id  (int)   : Product_Id of product 
    
        Returns:
        Response    (dict)  : Contains Product_Id and Message 
        '''
        dic = {}
        try:
            print('In delete')
            # Check whether Product_Id is valid or not
            try:
                pk = int(pk)
            except:
                raise InvalidInputException
            
            # Update product details from database
            productDeleteStatus = ProductInventory.objects.filter(product_Id = pk).delete()
            
            # Check whether given product_Id is exists or not
            if productDeleteStatus[0] == 0:
                raise WrongInputException

            print('Product deleted successfully.')
            dic['data'] = {'product_Id': pk}
            dic['message'] = 'Product deleted successfully.'
        except (InvalidInputException, WrongInputException) as e:
            print('In Viewset_Inventory => deleted', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = e.description
        except Exception as e:
            print('In Viewset_Inventory => deleted', e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            dic['message'] = '''Product can't be deleted.'''
        dic['status'] = 200
        return Response(data=dic)
    