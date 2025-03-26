/**
 * Imports from modules
 */
import * as dotEnv from 'dotenv';
import * as path from 'node:path';
import mysql from 'mysql2/promise';
import fastify from 'fastify';
import express from 'express';

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
 * @param useFastify - use fastify instead of Express
 * @returns {Promise<void>}
 */
function startServer(useFastify) {
    let amount = 0;
    console.log(useFastify ? 'Fastify started' : 'Express started')

    const app = useFastify ? fastify() : express();

    app.get('/endpoint_slow', async (req, res) => {
        amount++;
        try {
            const result = await getData();
            await updateAmount(amount)
            const response = { amount, result };

            res.status(200).send(response);
        } catch (error) {
            res.status(500).send({ error: 'Database error' });
        }
    });

    app.get('/endpoint_fast', async (req, res) => {
        amount++;
        res.status(200).send({amount});
    });

    app.listen({port: PORT, host: '0.0.0.0'}, () => {
        console.log(`Process ${process.pid} started on port ${PORT}`);
    });
}


/**
 * Start application
 * @param useFastify - use fastify instead of Express
 */
export async function start(useFastify) {
    startServer(useFastify);
    updateAmount(0);
}