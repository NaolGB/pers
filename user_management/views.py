from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Department, Profile, UserAccessLevel, Company
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import ProfileFormEditProfile
from user_management.user_access_control import has_role, has_access_level, get_redirect

def company_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        access_level = UserAccessLevel.SUPERUSER  

        # Validate user and company data
        if not (username and password and company_name):
            return render(request, 'user_management/company_signup.html', {'error_message': 'Invalid data'})

        # Check if a user with the same username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'user_management/company_signup.html', {'error_message': 'Username already taken'})

        # Check if a company with the same name already exists
        if Company.objects.filter(name=company_name).exists():
            return render(request, 'user_management/company_signup.html', {'error_message': 'Company name already taken'})

        # All validation checks passed, create user and company
        user = User.objects.create_user(username=username, password=password)
        company = Company.objects.create(name=company_name, creator=user)

        # Create a superuser department and assign it to the user's profile
        superuser_department = Department.objects.create(name='Superuser', company=company)
        profile = Profile.objects.create(user=user, company=company, department=superuser_department, access_level=access_level)

        return redirect('user_login')

    return render(request, 'user_management/company_signup.html')

def user_login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        # invalid login credentials
        if user is None: 
            error_message = 'Invalid login credentials'
            return render(request, 'user_management/login.html', {'error_message': error_message})

        # no profile created
        if not Profile.objects.filter(user=user).exists():
            error_message = 'User does not have a profile'
            return render(request, 'user_management/login.html', {'error_message': error_message})
        
        # successful login
        login(request, user)
        return redirect(get_redirect(user))
        
    # logout
    elif request.method == 'GET' and request.user.is_authenticated:
        logout(request)
        return redirect('user_login')

    return render(request, 'user_management/login.html', {'error_message': error_message})

@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER])
)
def create_user_department_profile(request):
    error_message = None

    # Get the logged-in user's company
    try:
        profile = request.user.profile
        company = profile.company
    except Profile.DoesNotExist:
        error_message.append("Profile does not exist")

    if request.method == 'POST':
        # create or add department
        department_id = request.POST.get('department')
        new_department_name = request.POST.get('new_department')

        if department_id:
            department = Department.objects.get(id=department_id)
        elif new_department_name:
            department, created = Department.objects.get_or_create(name=new_department_name, company=company)
        else:
            error_message = "Please select an existing department or enter a new department name."
            return render(
                request, 
                'user_management/create_user.html', 
                {'error_message': error_message}
            )

        # validate employee id
        employee_id = request.POST['employee_id']
        if Profile.objects.filter(employee_id=employee_id).exists():
            error_message = "Employee ID already exists. Please choose a different Employee ID."
            return render(
                request, 
                'user_management/create_user.html', 
                {'error_message': error_message}
            )
        access_level = request.POST['access_level']

        # create user, after department and employee id to ensure no user is created 
        # without valid department and employee id
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
            return render(
                request, 
                'user_management/create_user.html', 
                {'error_message': error_message}
            )
        password = request.POST['password']

        if error_message is None:
            user = User.objects.create_user(username=username, password=password)

            profile = Profile.objects.create(
                user=user,
                employee_id=employee_id,
                department=department,
                access_level=access_level,
                company=company,  # Assign the logged-in user's company
            )

            return redirect('power_user_dashboard')

    context = {
        'existing_department': Department.objects.filter(company=company),
        'user_access_level': UserAccessLevel.choices,
        'error_message': error_message,  # Pass the error_message messages to the template
    }
    return render(request, 'user_management/create_user.html', context)

@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER])
)
def power_user_dashboard(request):
    context = {
        'profiles': Profile.objects.all()
    }

    return render(request, 'user_management/power_user_dashboard.html', context)

@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER])
)
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    if request.method == 'POST':
        form = ProfileFormEditProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('power_user_dashboard')
    else:
        form = ProfileFormEditProfile(instance=profile)

    context = {
        'form': form, 
        'profile': profile,
    }
    return render(request, 'user_management/edit_profile.html', context)