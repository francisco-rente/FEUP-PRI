import logo from "./logo.svg";
import "./App.css";
import {FaAmazon} from "react-icons/fa";
import axios from 'axios';
var ReactDOM = require('react-dom');



const root = ReactDOM.createRoot(document.getElementById('root'));
let books = [];
let numFound = 0;
let current_url = "";
let current_filter = "";
let facets = [];
let previous_searchs = "";
const proxy = "http://127.0.0.1:8000/"

function getQuerryTermFromURL(url){
    let query_terms = url.split("q=")[1].split("%3A")[0]
    return decodeURIComponent(query_terms)
}

function App() {
    return (
        <>
            <div className="w-full"
                onClick={() => {
                    window.location.href = "http://localhost:3000";
                }}
            >
                <h1 className="text-7xl m-12 font-sans font-bold">
                    KindleMe<span className="text-[#ff9900]">Some</span>{" "}
                    <FaAmazon className="inline text-[#ff9900]"/>
                </h1>
            </div>
            <div className="App">
                <div className="container">
                    <SearchBar/>
                    <div className="flex">
                        <div
                            className="w-1/3 mr-12 p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                            <Filters/>
                        </div>
                        <div
                            className="h-36 w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                            <Results/>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}


function createURL() {
    const default_url = "http://localhost:8983/solr/kindle/select?defType=edismax&indent=true&q.op=OR&qf=title&q=";

    const search_value = document.getElementById("default-search").value;
    
    if (search_value === "") {
        return default_url + "*";
    }
    

    const query = encodeURIComponent(search_value);
    const query_url = default_url + query;
    current_url = query_url;
    return current_url;
}


async function searchRequest(event) {
    event.preventDefault()
    let url = createURL();
    if (!url) return null;

    // if filter is active 

    url +="&fq=type%3Abook";
    let current_search = document.getElementById("default-search").value == "" ? '*' :  document.getElementById("default-search").value 

    if(previous_searchs === current_search){
        if(facets.some((facet) => facet.checked)){
            for (let filter of facets){
                if(filter.checked){
                    console.log(filter.facet);
                    url += "%2C%20category%3A" + filter.facet;
                }
            }
        }
    }


    const json_body = {"url": url}
    const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};
    const response = await axios.post(proxy, json_body, {headers: headers});
    books = response.data.response.docs;
    numFound = response.data.response.numFound;
    

    if(previous_searchs !== current_search){
        const facets_body = {"url": url + "&facet=true&facet.field=brand&facet.field=category&facet.field=overall"}
        const facets_response = await axios.post(proxy, facets_body, {headers: headers});
        const retrieved_facets = facets_response.data.facet_counts.facet_fields["category"];
        facets = [];
        for (let i = 0; i < retrieved_facets.length; i++) {
            if(retrieved_facets[i+1])
            facets.push({"facet": retrieved_facets[i], "num": retrieved_facets[i+1], "checked": false});
            i += 1;
        }
        previous_searchs = current_search;
    }   

    root.render(<App />);
}


const Filters = () => {
   // filter are facets
   return (
         <div className="flex flex-col">
            <h1 className="text-2xl font-bold">Filters</h1>
            <div className="flex flex-col">
                {facets.map((facet) => (
                    <div className="flex flex-row">
                        <p className="text-sm">{facet.facet}</p>
                        <p className="text-sm"> ({facet.num})</p>
                        <input type="checkbox" id={facet.facet} name={facet.facet} value={facet.facet}
                        
                        onClick = {() => {
                            facet.checked = !facet.checked;
                        }}
                        
                        />
                    </div>
                ))}
            </div>
        </div>
    );
}


const Results = () => {
    console.log(books);
    return (
        <div className="flex flex-col">
            {books.map((book) => (
                <div className="flex flex-row"
                    onClick = {() => {
                        // open new tab 
                        window.open("http://www.amazon.com/exec/obidos/ASIN/" + book.id);
                    }}

                >
                    <div className="w-1/3">
                        <img src={book.imgUrl
                            ? book.imgUrl
                            : "https://via.placeholder.com/150"} alt="book cover"/>
                    </div>
                    <div className="w-2/3">
                        <h1 className="text-2xl font-bold">{book.title}</h1>
                        <h2 className="text-lg font-bold">{book.brand}</h2>
                        <p className="text-sm">{book.description}</p>
                        <p className="text-sm">{book.price ? book.price : -1}</p>
                        <p className="text-sm">{book.overall}</p>
                        <p className="text-sm">{book.category}</p>
                    </div>
                </div>
            ))}
        </div>
    );
}


const SearchBar = () => {
    return (
        <form className="mb-8">
            <label
                for="default-search"
                class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
            >
                Search
            </label>
            <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <svg
                        aria-hidden="true"
                        class="w-5 h-5 text-gray-500 dark:text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                        ></path>
                    </svg>
                </div>
                <input
                    type="search"
                    id="default-search"
                    class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Search for Books..."
                    required
                />
                <button
                    // type="submit"
                    class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                    onClick={searchRequest}
                >
                    Search
                </button>
            </div>
        </form>
    );
}


export default App;
