from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, Doctor, Appointment
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def home(request):
    return render(request, 'home.html')

def patient(request):
    return render(request, 'patient.html')

def register_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        age = request.POST.get('age')

        if not username or not email or not password or not gender:
            messages.error(request, 'All fields are required.')
            return redirect('p_register')
        
        try:
            age = int(age)
        except ValueError:
            messages.error(request, 'Age must be a number.')
            return redirect('p_register')
        
        if age < 18:
            messages.error(request, 'You must be at least 18 years old to register.')
            return redirect('p_register')

        if Patient.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            Patient.objects.create_user(username=username, email=email, password=password ,gender=gender, age=age)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login_patient')
    return render(request, 'p_register.html')

def login_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use email for authentication
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, 'You have successfully logged in.')
            return redirect('patient')  # Redirect to the patient dashboard
        else:
            messages.error(request, 'Invalid username or password.')  # Show error message
    return render(request, 'patient.html')

def p_register(request):
    return render(request, 'p_register.html')

def doctor_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        city = request.POST['city']
        age = request.POST['age']
        specialty = request.POST['specialty']
        clinic_address = request.POST['clinic_address']
        experience_years = request.POST['experience_years']

        if Doctor.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            Doctor.objects.create(
                name=name,
                email=email,
                password=password,
                gender=gender,
                city=city,
                age=age,
                specialty=specialty,
                clinic_address=clinic_address,
                experience_years=experience_years,
            )
            messages.success(request, 'Account created successfully!')
            return redirect('doctor_login')
    return render(request, 'doctor_signup.html')

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use email instead of username
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(email=email, password=password)
            request.session['doctor_email'] = doctor.email 
            return redirect('doctor')  # Redirect to doctor dashboard
        except Doctor.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'doctor_login.html')

def doctor(request):
    # Assuming the doctor logs in with email
    email = request.session.get('doctor_email')
    doctor = Doctor.objects.filter(email=email).first()
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time') if doctor else []
    return render(request, 'doctor.html', {'doctor': doctor, 'appointments': appointments})

def search_doctors(request):
    if request.method == 'POST':
        specialty = request.POST.get('specialty')
        city = request.POST.get('city')
    else:
        specialty = request.GET.get('specialty')
        city = request.GET.get('city')
        print(f"Specialty: {specialty}, City: {city}")  # Debugging output
        

        # Filter doctors based on specialty and city
        doctors = Doctor.objects.filter(specialty=specialty, city=city)
        return render(request, 'search_results.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    times = []
    for hour in range(8, 18):  # 8:00 to 17:30
        times.append(f"{hour:02d}:00")
        times.append(f"{hour:02d}:30")
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        patient = Patient.objects.get(username=request.user.username)

        # Create the appointment
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time,
            status='Pending'
        )
        messages.success(request, f"Appointment with Dr. {doctor.name} on {date} at {time} was successfully booked and is now waiting for confirmation.")
        return redirect('patient')

    return render(request, 'book_appointment.html', {'doctor': doctor, 'times': times})

@login_required
def manage_appointments(request):
    try:
        doctor = Doctor.objects.get(email=request.user.email)  # Ensure the logged-in user is a doctor
        appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')
        return render(request, 'doctor.html', {'appointments': appointments})
    except Doctor.DoesNotExist:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')

def update_appointment_status(request, appointment_id):
    if request.method == 'POST':
        appointment = Appointment.objects.get(id=appointment_id)
        new_status = request.POST.get('status')
        reschedule_message = request.POST.get('reschedule_message', '')

        appointment.status = new_status
        if new_status == 'Rescheduled':
            appointment.reschedule_message = reschedule_message
        appointment.save()

        # Notify the patient
        if new_status == 'Rescheduled':
            messages.info(request, f"Appointment rescheduled to {appointment.date} at {appointment.time}.")
        elif new_status == 'Confirmed':
            messages.success(request, "Appointment confirmed.")
        elif new_status == 'Cancelled':
            messages.error(request, "Appointment cancelled.")
        elif new_status == 'Refused':
            messages.error(request, "Appointment refused.")

        return redirect('doctor')

def patient(request):
    patient = Patient.objects.get(username=request.user.username)
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')
    doctors = Doctor.objects.all()  # Pass all doctors to the template
    return render(request, 'patient.html', {'appointments': appointments, 'doctors': doctors})

@login_required
def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = Patient.objects.get(username=username)
            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, f"Password for user '{username}' has been updated successfully.")
            return redirect('p_register')  # Redirect to the patient dashboard
        except Patient.DoesNotExist:
            messages.error(request, f"User with username '{username}' does not exist.")

    return render(request, 'change_password.html')

def doctor_change_password(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            doctor = Doctor.objects.get(name=name)
            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            else:
                doctor.password = new_password  # For real security, hash the password!
                doctor.save()
                messages.success(request, f"Password for Dr. '{doctor.name}' has been updated successfully.")
                return redirect('doctor_login')
        except Doctor.DoesNotExist:
            messages.error(request, f"No doctor found with email '{name}'.")
    return render(request, 'doctor_change_password.html')

def medintroduction(request):
    return render(request, 'medintroduction.html')
