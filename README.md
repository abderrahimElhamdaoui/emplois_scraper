<html>
    <body>
        <h2>Objectif  </h2>
         <p>
            Ce script est conçu pour scraper les offres de stages depuis le site MyJobAlert.ma en utilisant Scrapy pour la gestion des requêtes et Splash pour le rendu des pages dynamiques (JavaScript). 
            Les données des offres sont collectées et exportées dans un fichier Excel nommé job_offers.xlsx.
          </p>
          <br>
          <h2>Principales Fonctionnalités </h2>
           <ul>
            <li>
                <h4>Initialisation</h4>
                <ul>
                    <li>La classe s'appelle EmploisScraper et utilise Scrapy comme framework de scraping.</li>
                    <li>Elle utilise un fichier Excel pour stocker les données collectées.</li>
                </ul>
            </li>
            <li>
                <h4>Points de départ</h4>
                <ul>
                    <li>La requête commence à partir de l'URL spécifiée dans start_urls (https://myjobalert.ma/jobs/?contract=stage).</li>
                </ul>
            </li>
            <li>
                <h4>Lua Scripts</h4>
                <ul>
                    <li>lua_script : Charge la page principale des offres de stages.</li>
                    <li>lua_script2 : Charge les détails de chaque offre</li>
                </ul>
            </li>
            <li>
                <h4>Extraction des Données (Méthode parse)</h4>
                <ul>
                    <li>Le script récupère les offres à partir des blocs HTML (div.w-full.md\:w-3\/6.mx-1.flex.flex-col).</li>
                    <li>
                        Pour chaque offre
                        <ul>
                            <li>Titre, lien, informations sur l'entreprise, localisation, et vérification sont extraits.</li>
                            <li>Si ces données sont valides, une requête Splash est effectuée pour scraper les détails.</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li>
                <h4>Scraping des Détails (Méthode parse_job_details)</h4>
                <ul>
                    <li>Une fois la page d'une offre chargée, des informations supplémentaires sont extraites : ype de contrat, type d'offre, ville, expérience requise, et description.</li>
                    <li>Ces données sont combinées avec celles déjà collectées.</li>
                </ul>
            </li>
            <li>
                <h4>Pagination</h4>
                <ul>
                    <li>Le script identifie le lien de la page suivante (via a.w-auto.p-2.px-4.bg-white.border-2::attr(href)) et continue le scraping jusqu'à ce qu'il n'y ait plus de pages.</li>
                </ul>
            </li>
            <li>
                <h4>Sauvegarde des Données</h4>
                <ul>
                    <li>Les données collectées sont stockées dans une liste self.jobs, converties en un DataFrame Pandas, et exportées en fichier Excel (job_offers.xlsx).</li>
                </ul>
            </li>
           </ul>
           <hr>
           <h2>Structure des Données Exportées</h2>
           <h3>Le fichier Excel contiendra les colonnes suivantes </h3>
           <ul>
                <li>title : Titre de l'offre.</li>
                <li>link : Lien vers l'offre.</li>
                <li>company_info : Informations sur l'entreprise.</li>
                <li>location : Localisation.</li>
                <li>verified : Indicateur si l'offre est vérifiée.</li>
                <li>contract : Type de contrat (Stage, CDI, etc.).</li>
                <li>type : Type de poste.</li>
                <li>ville : Ville où le poste est basé.</li>
                <li>experience : Années d'expérience requises.</li>
                <li>description : Description complète de l'offre.</li>
            </ul>
            <br>
            <h3>Points Forts</h3>
            <ul>
                <li>Utilisation de Splash pour scraper des pages nécessitant un rendu JavaScript.</li>
                <li>Gestion de la pagination pour parcourir plusieurs pages de résultats.</li>
                <li>Exportation organisée et réutilisable des données dans un fichier Excel.</li>
            </ul>
    </body>
 </html>