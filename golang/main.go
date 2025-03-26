package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"runtime"

	_ "github.com/go-sql-driver/mysql"
)

var db *sql.DB
var amount int

// Database connection
func initDB() (*sql.DB, error) {
	dbUser := os.Getenv("MYSQL_USER")
	dbPass := os.Getenv("MYSQL_PASSWORD")
	dbHost := os.Getenv("MYSQL_HOST")
	dbSchema := os.Getenv("MYSQL_SCHEMA")
	dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s", dbUser, dbPass, dbHost, dbSchema)

	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, err
	}

	if err := db.Ping(); err != nil {
		return nil, err
	}

	return db, nil
}

// Return data from database
func getData() (map[string]interface{}, error) {
	var result map[string]interface{}
	query := "SELECT * FROM test WHERE name = ? LIMIT 1"
	rows, err := db.Query(query, "amount")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var id int
		var name, code string
		if err := rows.Scan(&id, &name, &code); err != nil {
			return nil, err
		}
		result = map[string]interface{}{"id": id, "name": name, "code": code}
	}

	return result, nil
}

// Update query amount in database
func updateAmount(newAmount int) error {
	query := "UPDATE test SET code = ? WHERE name = 'amount'"
	_, err := db.Exec(query, newAmount)
	return err
}

// HTTP method handler
func handler(w http.ResponseWriter, r *http.Request) {
	switch r.URL.Path {
	case "/endpoint_slow":
		if r.Method == http.MethodGet {
			amount++
			result, err := getData()
			if err != nil {
				http.Error(w, fmt.Sprintf("Database error: %s", err), http.StatusInternalServerError)
				return
			}

			updateAmount(amount)

			response := map[string]interface{}{"amount": amount, "result": result}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			json.NewEncoder(w).Encode(response)
		} else {
			http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		}

	case "/endpoint_fast":
		amount++
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]interface{}{"amount": amount})

	default:
		http.Error(w, "Not Found", http.StatusNotFound)
	}
}

// Start HTTP server
func startServer() {
	port := os.Getenv("GO_PORT")
	if port == "" {
		port = "3000"
	}
	http.HandleFunc("/endpoint_slow", handler)
	http.HandleFunc("/endpoint_fast", handler)

	runtime.GOMAXPROCS(1)

	fmt.Println(fmt.Sprintf("Server started on port %s", port))

	if err := http.ListenAndServe(fmt.Sprintf(":%s", port), nil); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}

// Start app
func main() {
	// err := godotenv.Load("../env/.env")
	// if err != nil {
	// 	log.Fatal("Error loading .env file")
	// }

	var errDB error
	db, errDB = initDB()
	if errDB != nil {
		log.Fatalf("Error initializing DB: %v", errDB)
	}

	startServer()
}
