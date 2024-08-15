import os

def generate_auth():
    os.makedirs("output/auth/Middleware", exist_ok=True)
    os.makedirs("output/auth/Controllers/Auth", exist_ok=True)
    os.makedirs("output/auth/Models", exist_ok=True)
    os.makedirs("output/auth/resources/views/auth", exist_ok=True)
    
    # Middleware template
    middleware_template = """<?php

namespace App\\Http\\Middleware;

use Closure;
use Illuminate\\Support\\Facades\\Auth;

class Authenticate
{
    /**
     * Handle an incoming request.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @param  \\Closure  $next
     * @param  string|null  ...$guards
     * @return mixed
     */
    public function handle($request, Closure $next, ...$guards)
    {
        if (Auth::check()) {
            return $next($request);
        }

        return redirect()->route('login');
    }
}
"""
    with open("output/auth/Middleware/Authenticate.php", "w") as file:
        file.write(middleware_template)
    
    # Auth Controller template
    auth_controller_template = """<?php

namespace App\\Http\\Controllers\\Auth;

use App\\Http\\Controllers\\Controller;
use App\\Models\\User;
use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Auth;
use Illuminate\\Support\\Facades\\Hash;
use Illuminate\\Support\\Facades\\Validator;

class AuthController extends Controller
{
    public function showLoginForm()
    {
        return view('auth.login');
    }

    public function showRegisterForm()
    {
        return view('auth.register');
    }

    public function showResetPasswordForm()
    {
        return view('auth.passwords.reset');
    }

    public function login(Request $request)
    {
        $credentials = $request->only('email', 'password');

        if (Auth::attempt($credentials)) {
            return redirect()->intended('dashboard');
        }

        return redirect()->back()->withErrors(['email' => 'Invalid credentials.']);
    }

    public function register(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
        ]);

        if ($validator->fails()) {
            return redirect()->route('register')
                             ->withErrors($validator)
                             ->withInput();
        }

        User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);

        return redirect()->route('login')->with('success', 'Registration successful. Please login.');
    }

    public function resetPassword(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'email' => 'required|string|email|max:255',
            'password' => 'required|string|min:8|confirmed',
        ]);

        if ($validator->fails()) {
            return redirect()->route('password.request')
                             ->withErrors($validator)
                             ->withInput();
        }

        $user = User::where('email', $request->email)->first();
        if ($user) {
            $user->password = Hash::make($request->password);
            $user->save();
            return redirect()->route('login')->with('success', 'Password reset successful. Please login.');
        }

        return redirect()->route('password.request')->withErrors(['email' => 'Email not found.']);
    }

    public function logout()
    {
        Auth::logout();
        return redirect()->route('login');
    }
}
"""
    with open("output/auth/Controllers/Auth/AuthController.php", "w") as file:
        file.write(auth_controller_template)
    
    # User Model template
    user_model_template = """<?php

namespace App\\Models;

use Illuminate\\Foundation\\Auth\\User as Authenticatable;
use Illuminate\\Notifications\\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'name', 'email', 'password',
    ];

    /**
     * The attributes that should be hidden for arrays.
     *
     * @var array
     */
    protected $hidden = [
        'password', 'remember_token',
    ];
}
"""
    with open("output/auth/Models/User.php", "w") as file:
        file.write(user_model_template)
    
    # Login template
    login_template = """@extends('layouts.app')

@section('content')
    <div class="container">
        <h4 class="fw-bold py-3 mb-4">Login</h4>
        <form action="{{ route('login') }}" method="POST">
            @csrf
            @if ($errors->any())
                <div class="alert alert-danger">
                    <ul>
                        @foreach ($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" name="email" id="email" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" name="password" id="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
@endsection
"""
    with open("output/auth/resources/views/auth/login.blade.php", "w") as file:
        file.write(login_template)
    
    # Register template
    register_template = """@extends('layouts.app')

@section('content')
    <div class="container">
        <h4 class="fw-bold py-3 mb-4">Register</h4>
        <form action="{{ route('register') }}" method="POST">
            @csrf
            @if ($errors->any())
                <div class="alert alert-danger">
                    <ul>
                        @foreach ($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" name="name" id="name" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" name="email" id="email" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" name="password" id="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
    </div>
@endsection
"""
    with open("output/auth/resources/views/auth/register.blade.php", "w") as file:
        file.write(register_template)
    
    # Reset Password template
    reset_password_template = """@extends('layouts.app')

@section('content')
    <div class="container">
        <h4 class="fw-bold py-3 mb-4">Reset Password</h4>
        <form action="{{ route('password.update') }}" method="POST">
            @csrf
            @if ($errors->any())
                <div class="alert alert-danger">
                    <ul>
                        @foreach ($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" name="email" id="email" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">New Password</label>
                <input type="password" name="password" id="password" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="password_confirmation" class="form-label">Confirm Password</label>
                <input type="password" name="password_confirmation" id="password_confirmation" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Reset Password</button>
        </form>
    </div>
@endsection
"""
    with open("output/auth/resources/views/auth/passwords/reset.blade.php", "w") as file:
        file.write(reset_password_template)


