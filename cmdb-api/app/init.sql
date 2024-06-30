-- Create the users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE
);

-- Create the virtual_machines table
CREATE TABLE virtual_machines (
    vm_name VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    memory_gb INTEGER,
    cpu_cores INTEGER,
    os_type VARCHAR(255)
);

-- Create the relationship between users and virtual_machines
ALTER TABLE virtual_machines ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(user_id);

