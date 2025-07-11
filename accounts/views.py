from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .forms import (
    UserRegisterForm, CustomAuthenticationForm, CustomPasswordResetForm,
    CustomSetPasswordForm, UserProfileUpdateForm
)
from .models import CustomUser

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = True
                user.email_verified = False
                user.save()

                # Generate verification token
                uid = user.get_uid()
                token = user.get_verification_token()
                
                # Build verification URL
                current_site = request.get_host()
                verification_url = f"http://{current_site}/accounts/verify-email/{uid}/{token}/"
                
                # Prepare email
                context = {
                    'user': user,
                    'verification_url': verification_url,
                }
                html_message = render_to_string('accounts/email/verification.html', context)
                plain_message = strip_tags(html_message)
                
                try:
                    # Send verification email
                    email = EmailMultiAlternatives(
                        'Verify your email address',
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                    )
                    email.attach_alternative(html_message, "text/html")
                    email.send(fail_silently=False)
                    print(f"Verification email sent successfully to {user.email}")
                    
                    messages.success(request, 'Account created successfully! Please check your email to verify your account.')
                    return redirect('login')
                except Exception as e:
                    print(f"Failed to send verification email: {str(e)}")
                    messages.error(request, 'Failed to send verification email. Please try again or contact support.')
                    user.delete()  # Delete the user if email sending fails
                    return redirect('register')
                    
            except Exception as e:
                print(f"Error during registration: {str(e)}")
                messages.error(request, 'An error occurred during registration. Please try again.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        # Decode the UID from base64
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Check if the user exists and token is valid
    if user is not None and default_token_generator.check_token(user, token):
        if user.email_verified:
            messages.info(request, 'Your email has already been verified.')
        else:
            # Mark email as verified
            user.email_verified = True
            user.save()
            
            # Send welcome email
            context = {
                'user': user,
                'login_url': request.build_absolute_uri(reverse_lazy('login'))
            }
            html_message = render_to_string('accounts/email/welcome.html', context)
            plain_message = strip_tags(html_message)
            
            email = EmailMultiAlternatives(
                'Welcome to our platform!',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            messages.success(request, 'Email verified successfully! You can now log in.')
        
        return redirect('login')
    else:
        messages.error(request, 'The verification link is invalid or has expired.')
        return redirect('verification_failed')


def verification_failed(request):
    return render(request, 'accounts/verification_failed.html')


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        if not user.email_verified:
            messages.warning(self.request, 'Please verify your email before logging in.')
            return redirect('login')
        
        return super().form_valid(form)
        
    def get_success_url(self):
        """Return the URL to redirect to after successful login."""
        url = self.get_redirect_url()
        if url:
            return url
        # Redirect to user's own profile page
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})
        
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to catch CSRF errors and provide a better error message."""
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            if 'CSRF' in str(e):
                messages.error(request, 'CSRF verification failed. This could be due to your session expiring or browser security settings. Please try again.')
                return self.render_to_response(self.get_context_data())
            raise


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/email/password_reset.html'
    html_email_template_name = 'accounts/email/password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(settings, 'SITE_NAME'):
            context['site_name'] = settings.SITE_NAME
        if hasattr(settings, 'SITE_DOMAIN'):
            context['site_domain'] = settings.SITE_DOMAIN
        return context
        
    def form_valid(self, form):
        """Override to add custom context to the email."""
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': {
                'site_domain': settings.SITE_DOMAIN,
                'site_name': settings.SITE_NAME,
            },
        }
        form.save(**opts)
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        is_self = request.user == user
    else:
        user = request.user
        is_self = True
    
    if request.method == 'POST' and is_self:
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile', username=user.username)
    elif is_self:
        form = UserProfileUpdateForm(instance=user)
    else:
        form = None
    
    context = {
        'profile_user': user,
        'is_self': is_self,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    return profile(request)


def test_email(request):
    try:
        # Send a test email
        subject = 'Test Email'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = settings.EMAIL_HOST_USER
        text_content = 'This is a test email from your Django application.'
        html_content = '<h1>Test Email</h1><p>This is a test email from your Django application.</p>'
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        
        messages.success(request, 'Test email sent successfully!')
    except Exception as e:
        messages.error(request, f'Failed to send test email. Error: {str(e)}')
    
    return redirect('login')


def custom_logout(request):
    """Custom logout view to handle any pre-logout actions"""
    # Clear any custom session data if needed
    for key in list(request.session.keys()):
        if not key.startswith('_'):  # Don't remove Django's session keys
            del request.session[key]
    
    # Perform the logout
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')
