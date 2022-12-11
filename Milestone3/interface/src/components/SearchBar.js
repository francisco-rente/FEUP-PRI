import axios from "axios";

const proxy = "http://127.0.0.1:8000/"

const SearchBar = (props) => {
    
    function fetchSuggestions(event)  {
        const query = event.target.value;
        
        const url = "http://localhost:8983/solr/kindle/suggest?defType=edismax&fq=type%3Abook&indent=true&q.op=OR&q=" + query + "&qf=title&rows=4&sort=overall%20asc&start=0";
        const json_body = {"url": url}
        const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};
        axios.post(proxy, json_body, {headers: headers}).then((response) => {
            const result = response.data.suggest.mySuggester[query].suggestions.map((suggestion) => suggestion.term)
            props.setSearch(result.slice(0,5));
        })
    }
    return (
        <div className="mb-8">
        <div>
            <label
                for="default-search"
                class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
            >
                {}
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
                    onChange = {(event) => {
                        fetchSuggestions(event);
                        props.setBookInput(event.target.value);
                    }}
                    value={props.bookInput}
                />
                

                

                <div className="flex flex-row">
                </div>
                <button
                    class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                    onClick={() => {
                        console.log("MAKING REQUEST");
                        props.searchRequest();
                        props.setSearch([]);
                    }}
                >
                    Search
                </button>
            </div>
            
        </div>
        
        {props.search.length > 0 && 
        <ul className="py-4 text-left bg-slate-200">
        {props.search.map((suggestion,index) => (
            <li className="text-lg pl-4 hover:bg-slate-400 py-1" onClick={() => {
                props.setBookInput('"'+suggestion +'"');

            }}>{suggestion}</li>
        ))}
        </ul>}
        

        </div>
    );
}

export default SearchBar;