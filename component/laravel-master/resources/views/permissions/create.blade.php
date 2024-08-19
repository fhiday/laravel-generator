@extends('layouts.app')

@section('content')
    <div class="container">

        @if (session('success'))
            <div class="alert alert-success">
                {{ session('success') }}
            </div>
        @endif
        <div class="card mb-4">
            <div class="card-body">
                <form action="{{ route('permissions.store') }}" method="POST">
                    @csrf
                    <div class="mb-3"><label for="name" class="form-label">Name</label><input type="text" name="name" id="name" class="form-control" required></div><div class="mb-3"><label for="guard_name" class="form-label">Guard_name</label><input type="text" name="guard_name" id="guard_name" class="form-control" required></div>
                    <a href="{{ route('permissions.index') }}" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </a>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    </div>
@endsection
