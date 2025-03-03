from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404, redirect
from plants.form import CustomerUserForm
from django.contrib import messages
from .models import Catagory, Product
from django.contrib.auth import authenticate,login,logout
from .models import Cart
from django.db.models import Q



# ----- HOME PAGE -----

def home(request):
    trending_products = Product.objects.filter(trending=True, Catagory__isnull=False)
    for product in trending_products:
        print(f"Product: {product.name}, Category: {product.Catagory.name if product.Catagory else 'None'}")
    return render(request, 'index.html', {"trending_products": trending_products})

# ----- LOGOUT PAGE -----

def logout_page(request):
    if request.user.is_authenticated:  
        logout(request)
        messages.success(request, "Logged Out Successfully")
    return redirect("/")

# ----- LOGIN PAGE -----

def login_page(request):
    if request.user.is_authenticated:  
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged In Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name and Password")
                return redirect("/login")
        return render(request, 'login.html')

# ----- SIGNIN PAGE -----

def register(request):
    form=CustomerUserForm()
    if request.method=='POST':
        form=CustomerUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Signin Success You Can Login Now...!")
            return redirect('/login')
    return render(request, 'register.html',{'form':form})

# ----- BLOGS PAGE -----

def blogs(request):
    categories = Catagory.objects.filter(status=0) 
    return render(request, 'blogs.html', {"categories": categories})

# ----- BLOGSVIEW PAGE -----

def blogsview(request, name):
    category = get_object_or_404(Catagory, name=name)
    products = Product.objects.filter(Catagory=category)
    for product in products:
        if not product.product_image:
            print(f"Product {product.name} has no image.")
    return render(request, 'products/blogsview.html', {"category": category, "products": products})

# ----- product_details PAGE -----

def product_details(request, cname, pname):
    print(f"Category Name: {cname}")  # Debug statement
    print(f"Product Name: {pname}")  # Debug statement

    category = Catagory.objects.filter(name=cname, status=0).first()
    if category:
        product = Product.objects.filter(name=pname, status=0, Catagory=category).first()
        if product:
            return render(request, 'products/product_details.html', {"product": product})
        else:
            messages.error(request, "No Such Product Found")
            return redirect('blogs')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('blogs')
    

# ----- ADD TO CART PAGE -----


@csrf_exempt
def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_qty = data.get('product_qty')
                product_id = data.get('pid')

                print(f"Received Product ID: {product_id}, Quantity: {product_qty}")

                if not product_id or not product_qty:
                    return JsonResponse({'status': 'Invalid Data'}, status=400)

                product = Product.objects.get(id=product_id)
                user = request.user

                cart_item, created = Cart.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={'product_qty': product_qty}
                )

                if not created:
                    cart_item.product_qty += product_qty
                    cart_item.save()

                print(f"Cart updated for {user.username}: {cart_item.product_qty} items of {product.name}")
                return JsonResponse({'status': 'Success', 'product_qty': cart_item.product_qty, 'pid': product_id}, status=200)

            except Product.DoesNotExist:
                print("Product Not Found")
                return JsonResponse({'status': 'Product Not Found'}, status=404)

            except json.JSONDecodeError:
                print("Invalid JSON")
                return JsonResponse({'status': 'Invalid JSON'}, status=400)

        else:
            print("User not logged in")
            return JsonResponse({'status': 'Login To Add Cart'}, status=200)

    print("Invalid Request")
    return JsonResponse({'status': 'Invalid Access'}, status=400)


# ----- CART PAGE -----

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request, 'cart.html', {"cart": cart})
    else:
        return redirect("/")




def remove_cart(request, cid):
    cartitem = get_object_or_404(Cart, id=cid)
    cartitem.delete()
    return redirect('cart')


# ----- SEARCH PAGE -----


def search_products(request):
    query = request.GET.get('q')
    print(f"Search query: {query}")  # Debugging output
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.none()
    print(f"Found {products.count()} products")  # Debugging output
    return render(request, 'search_results.html', {'products': products, 'query': query})


# ----- PAYMENTS PAGE -----

def payment1(request):
    return render(request, 'payment1.html') 

def payment2(request):
    return render(request, 'payment2.html') 

def payment3(request):
    return render(request, 'payment3.html') 

def checkout(request):
    return render(request, 'checkout.html') 
