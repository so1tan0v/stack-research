/**
 * Imports from modules
 */
import * as dotEnv from 'dotenv';
import * as path from 'node:path';
import * as http from 'node:http';
import mysql from 'mysql2/promise';

dotEnv.config({
    path: [
        path.join(process.cwd(), 'env', '.env'),
        path.join(process.cwd(), '..', 'env', '.env')
    ]
});

const PORT = process.env.NODEJS_PORT || 3000;

const pool = mysql.createPool({
    host: process.env.MYSQL_HOST,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_SCHEMA,
    waitForConnections: true,
    connectionLimit: 50,
    queueLimit: 0
});

/**
 * Return data from database
 * @returns {Promise<*|null>}
 */
async function getData() {
    const connection = await pool.getConnection();
    try {
        const [results] = await connection.query(
            "SELECT * FROM test WHERE name = ? LIMIT 1", 
            ['amount']
        );
        return results.length > 0 ? results[0] : null;
    } finally {
        connection.release();
    }
}

/**
 * Update query amount in database
 * @param amount - Amount of query
 * @returns {Promise<*|null>}
 */
async function updateAmount(amount) {
    const connection = await pool.getConnection();
    try {
        const [results] = await connection.query(
            "UPDATE test SET code = ? WHERE name = 'amount'", 
            [amount]
        );
        return results.length > 0 ? results[0] : null;
    } finally {
        connection.release();
    }
}

/**
 * Method for HTTP server application
 * @returns {Promise<void>}
 */
async function startServer() {
    let amount = 0;

    const server = http.createServer(async (req, res) => {
        if (req.method === 'GET' && req.url === '/endpoint_slow') {
            amount++;

            try {
                const result = await getData();
                await updateAmount(amount)
                const response = { amount, result };

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(response));
            } catch (error) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Database error' }));
            }
        } else if(req.method === 'GET' && req.url === '/endpoint_fast') {
            amount++
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ amount }));
        }
    });


    server.keepAliveTimeout = 5 * 1000;
    server.headersTimeout = 6 * 1000;

    server.listen(PORT, '0.0.0.0', () => {
        console.log(`Process ${process.pid} started on port ${PORT}`);
    });
}

startServer();
