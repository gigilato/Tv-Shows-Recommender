package com.gm.gislain.tvshowapp.Model;

import java.util.ArrayList;

/**
 * Created by Gislain on 25/11/2016.
 */

public class Show {

    private int id;
    private String name;
    private String poster;
    private String overview;
    private String type;
    private String language;
    private Integer seasons;
    private Integer episodes;
    private Integer runtime;
    private String status;
    private String date;
    private double popularity;
    private double votes;
    private String backdrop;
    private ArrayList<Creator> creators;
    private ArrayList<Actor> actors;
    private ArrayList<Network> networks;
    private ArrayList<Genre> genres;

    public static String KEY_ID = "id";
    public static String KEY_NAME = "name";
    public static String KEY_POSTER = "poster";
    public static String KEY_OVERVIEW = "overview";
    public static String KEY_TYPE = "type";
    public static String KEY_LANGUAGE = "language";
    public static String KEY_SEASONS = "seasons";
    public static String KEY_EPISODES = "episodes";
    public static String KEY_RUNTIME = "runtime";
    public static String KEY_STATUS = "status";
    public static String KEY_DATE = "airDate";
    public static String KEY_POPULARITY = "popularity";
    public static String KEY_VOTES = "votes";
    public static String KEY_ACTORS = "actors";
    public static String KEY_CREATORS = "creators";
    public static String KEY_NETWORKS = "networks";
    public static String KEY_GENRES = "genres";
    public static String KEY_BACKDROP = "backdrop";

    public Show() {}

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPoster() {
        return poster;
    }

    public void setPoster(String poster) {
        this.poster = poster;
    }

    public String getOverview() {
        return overview;
    }

    public void setOverview(String overview) {
        this.overview = overview;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public Integer getSeasons() {
        return seasons;
    }

    public void setSeasons(Integer seasons) {
        this.seasons = seasons;
    }

    public Integer getEpisodes() {
        return episodes;
    }

    public void setEpisodes(Integer episodes) {
        this.episodes = episodes;
    }

    public Integer getRuntime() {
        return runtime;
    }

    public void setRuntime(Integer runtime) {
        this.runtime = runtime;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public double getPopularity() {
        return popularity;
    }

    public void setPopularity(double popularity) {
        this.popularity = popularity;
    }

    public double getVotes() {
        return votes;
    }

    public void setVotes(double votes) {
        this.votes = votes;
    }

    public String getBackdrop() {
        return backdrop;
    }

    public void setBackdrop(String backdrop) {
        this.backdrop = backdrop;
    }

    public ArrayList<Creator> getCreators() {
        return creators;
    }

    public void setCreators(ArrayList<Creator> creators) {
        this.creators = creators;
    }

    public ArrayList<Actor> getActors() {
        return actors;
    }

    public void setActors(ArrayList<Actor> actors) {
        this.actors = actors;
    }

    public ArrayList<Network> getNetworks() {
        return networks;
    }

    public void setNetworks(ArrayList<Network> networks) {
        this.networks = networks;
    }

    public ArrayList<Genre> getGenres() {
        return genres;
    }

    public void setGenres(ArrayList<Genre> genres) {
        this.genres = genres;
    }
}
