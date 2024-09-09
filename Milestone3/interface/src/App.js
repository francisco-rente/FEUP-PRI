import logo from "./logo.svg";
import "./App.css";
import {FaAmazon} from "react-icons/fa";
import axios from 'axios';
import {useState, useEffect} from "react";
import SearchBar from "./components/SearchBar";
import NextPageButton from "./components/NextPageButton";
import BackPageButton from "./components/BackPageButton";
import Results from "./components/Results";
import Filters from "./components/Filters";


const proxy = "http://127.0.0.1:8000/"
const url = "http://localhost:8983/solr/kindle/"

function getQueryTermFromURL(url){
    let query_terms = url.split("q=")[1].split("%3A")[0]
    return decodeURIComponent(query_terms)
}

function App() {
    const [search, setSearch] = useState([]);
    const [bookInput, setBookInput] = useState("");
    const [books, setBooks] = useState([]);
    const [numFound, setNumFound] = useState(0);
    const [facets, setFacets] = useState([]);
    const [cursors, setCursors] = useState({
        "previous_cursor": ["*"],
        "current_cursor": "*",
        "next_cursor": "*"
    });

    const [previous_searchs, setPreviousSearchs] = useState("");

    function createFetchURL() {
        const default_url = url + "select?defType=edismax&rows=5&sort=id%20asc&cursorMark=" + cursors.current_cursor + "&indent=true&q.op=OR&qf=title&hl=on&hl.fl=title&q=";

        const search_value = bookInput
        
        if (search_value === "") {
            return default_url + "*";
        }
        
    
        const query = encodeURIComponent(search_value);
        const query_url = default_url + query;
        return query_url;
    }
    
    
    function searchRequest() {

        let url = createFetchURL(); 
        if (!url) return null;
    
        url +="&fq=type%3Abook";
        let current_search = bookInput ? document.getElementById("default-search").value :  '*'
        
        

        if(previous_searchs === current_search){
            console.log("same search");
            if(facets.some((facet) => facet.checked)){
                for (let filter of facets){
                    if(filter.checked){
                        console.log(filter.facet);
                        url += "%2C%20category%3A" + filter.facet;
                    }
                }
            }
        }
        else {
            setCursors({
                "previous_cursor": ["*"],
                "current_cursor": "*",
                "next_cursor": "*"
            });
            setFacets([]);
        }
    
        
        console.log(url);
        const json_body = {"url": url}
        const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};

        axios.post(proxy, json_body, {headers: headers}).then((response) => {
            console.log(response)
            let highlight = response.data.highlighting;
            let books_temp = response.data.response.docs;
            console.log("RESULTS" + books);
            for (let i = 0; i < books.length; i++) {
                books_temp[i].title = highlight[books_temp[i].id].title[0];
            }

            setBooks(books_temp);
            setNumFound(response.data.response.numFound);
            console.log(response.data.nextCursorMark);
            let temp_cursors = cursors 
            temp_cursors.next_cursor = response.data.nextCursorMark;
            setCursors(temp_cursors);
    
            console.log("previous_cursor: ", cursors.previous_cursor, "current_cursor: ", cursors.current_cursor, "next_cursor: ", cursors.next_cursor);
        });
    
        console.log("current_search is: ", current_search);
        console.log("previous_search is: ", previous_searchs);
        if(previous_searchs !== current_search){
            const facets_body = {"url": url + "&facet=true&facet.field=brand&facet.field=category&facet.field=overall"}
            axios.post(proxy, facets_body, {headers: headers}).then((facets_response) => {

                console.log(facets_response);

                const retrieved_facets = facets_response.data.facet_counts.facet_fields["category"];
                setFacets([]);
                let temp_facets = [];
                for (let i = 0; i < retrieved_facets.length; i++) {
                    if(retrieved_facets[i+1] == 0) break;
                    temp_facets.push({"facet": retrieved_facets[i], "num": retrieved_facets[i+1], "checked": false});
                    i += 1;
                }
                setFacets(temp_facets);
                setPreviousSearchs(current_search);
                console.log("previous_search is now: ", previous_searchs);
            });
        }   
        
    }
    
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
                <div className="container mb-4">
                    <SearchBar setBookInput={setBookInput} bookInput={bookInput} search={search} setSearch={setSearch} searchRequest={searchRequest}/>
                    <div className="flex">
                        <div> 
                            numFound: {numFound}
                        </div>
                    </div>
                    <div className="">
                        <div className="w-full mb-6">
                                <BackPageButton cursors = {cursors} setCursors={setCursors} searchRequest={searchRequest}/>
                                <NextPageButton cursors = {cursors} setCursors={setCursors} searchRequest={searchRequest}/>
                        </div>
                        <div className="flex justify-around">
                            <Filters facets={facets} setFacets={setFacets}/>
                            <Results books={books}/>
                        </div>
                        
                    </div>
                </div>
            </div>
        </>
    );
}



export default App;
