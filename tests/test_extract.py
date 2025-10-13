import pytest
import json
from src.extract import GuardianAPI, lambda_handler
from unittest.mock import patch, Mock
import logging

# ===== fixtures & variables =====
# Fixtures of Guardian API responses used for mocking. Return raw response.


@pytest.fixture
def mock_guardian_api_one_response():
    return {
  "response": {
    "status": "ok",
    "userTier": "developer",
    "total": 293,
    "startIndex": 1,
    "pageSize": 1,
    "currentPage": 1,
    "pages": 293,
    "orderBy": "newest",
    "results": [
      {
        "id": "us-news/2025/oct/13/firings-cdc-employees-reversed",
        "type": "article",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-10-13T15:48:51Z",
        "webTitle": "Firings of hundreds of CDC employees reportedly reversed",
        "webUrl": "https://www.theguardian.com/us-news/2025/oct/13/firings-cdc-employees-reversed",
        "apiUrl": "https://content.guardianapis.com/us-news/2025/oct/13/firings-cdc-employees-reversed",
        "blocks": {
          "body": [
            {
              "id": "68ed141c8f083e8202599caa",
              "bodyHtml": "\u003Cp\u003EThe firings of hundreds of employees at the Centers for Disease Control (CDC) have been reversed, according to several reports citing officials familiar with the matter, and the American Federation of Government Employees (AFGE), the largest union representing federal workers.\u003C/p\u003E \u003Cp\u003EOn Friday, the White House budget office \u003Ca href=\"https://www.theguardian.com/us-news/2025/oct/10/federal-workers-pay-government-shutdown\"\u003Eannounced\u003C/a\u003E that as a result of the ongoing government shutdown, reductions in force (RIFs) across agencies have begun.\u003C/p\u003E \u003Cp\u003EA spokesperson for the Department of Health and Human Services (HHS), which houses the CDC, initially said that all employees that received layoff notices “were designated non-essential by their respective divisions”.\u003C/p\u003E \u003Cp\u003EHowever, over the weekend, the administration rescinded more than half of the 1,300 termination notices it sent to public health officials at the CDC, according to \u003Ca href=\"https://www.axios.com/2025/10/13/trump-kennedy-cdc-firings-rehirings\"\u003EAxios\u003C/a\u003E and \u003Ca href=\"https://www.reuters.com/business/healthcare-pharmaceuticals/trump-administration-lays-off-dozens-cdc-officials-nyt-reports-2025-10-11/\"\u003EReuters\u003C/a\u003E, citing sources familiar. Around 600 people at the agency remain fired.\u003C/p\u003E \u003Cp\u003EOn Saturday, \u003Ca href=\"https://www.nytimes.com/2025/10/11/health/cdc-layoffs-measles.html\"\u003Ethe New York Times reported\u003C/a\u003E that members of the Epidemic Intelligence Service (EIS), informally known as “disease detectives”, as well as the team that compiles the widely respected scientific journal, the Morbidity and Mortality Weekly Report, were among the employees reinstated.\u003C/p\u003E \u003Cp\u003EInitially, around 70 members of EIS were laid off, according to the Times report. Also affected were Athalia Christie and Maureen Bartee, who are leading the federal response to the measles outbreak. The Times reported that the two infectious disease experts were laid off, only to receive an email saying that their firings “on or about” 10 October had been rescinded a day later.\u003C/p\u003E \u003Cp\u003EA senior administration official told the Times that the mistakenly fired workers “were sent incorrect notifications”, adding that “any correction has already been remedied”.\u003C/p\u003E \u003Cp\u003EA federal health official also \u003Ca href=\"https://abcnews.go.com/Politics/live-updates/government-shutdown-live-updates?id=126242587&amp;entryId=126436657&amp;userab=news_search_page_design_unification-429*variant_a_control_search-1786&amp;userab=news_search_page_design_unification-429*variant_b_search_redesign-1787\"\u003Etold ABC News\u003C/a\u003E that the mistake was due to a “coding error”. Neither the White House nor HHS have immediately responded to the Guardian’s requests for comment about how many employees have been recalled to their roles.\u003C/p\u003E \u003Cp\u003E“These firings are an assault on the health and lives of every person in the US,” said Gregg Gonsalves, an epidemiologist and member of Defend Public Health, a volunteer network of experts who work to challenge the Trump administration’s public health policies.\u003C/p\u003E \u003Cp\u003E“Did they not care enough to find out who they were firing and what they did before sending termination letters? The carelessness and callousness with which this administration handles life and death matters is unbelievable.”\u003C/p\u003E \u003Cp\u003EThe AFGE has filed a lawsuit against the Trump administration, seeking to block the firings across agencies. In a court filing, the government said that the layoffs across the federal workforce will impact over 4,000 employees. Later this week, a federal judge in San Francisco will hear arguments in the case.\u003C/p\u003E \u003Cp\u003EThe CDC has endured significant tumult in recent months. In August, a gunman targeted the agency’s headquarters in Atlanta, firing hundreds of bullets and killing a police officer in the attack. The perpetrator had blamed the Covid vaccine for making him depressed and suicidal.\u003C/p\u003E \u003Cp\u003EHealth secretary Robert F Kennedy Jr \u003Ca href=\"https://www.theguardian.com/us-news/2025/aug/28/rfk-resign-cdc-susan-monarez-fired\"\u003Ethen fired \u003C/a\u003Ethe recently appointed CDC director, Susan Monarez, after she spent less than a month on the job. Monarez’s removal has become an acrimonious flash point at the agency. At\u003Ca href=\"https://www.theguardian.com/us-news/2025/sep/17/cdc-director-susan-monarez-key-takeaways\"\u003E a Senate committee hearing\u003C/a\u003E, Monzarez said that Kennedy fired her for not complying with his vaccine agenda, adding that the health secretary had called the CDC the “most corrupt federal agency in the world”.\u003C/p\u003E \u003Cp\u003EFollowing her removal, several public health leaders \u003Ca href=\"https://www.theguardian.com/us-news/2025/aug/28/cdc-rally-staffers-protest\"\u003Eleft the agency\u003C/a\u003E in protest of political interference in their work. Debra Houry, the former chief medical officer at the CDC, said Kennedy “censored CDC science, politicized its processes and stripped leaders of independence” while speaking alongside Monarez on Capitol Hill last month.\u003C/p\u003E \u003Cp\u003E“Think about what it’s like to be at CDC. It’s like living with an abusive partner that attacks and then takes back some of the abuse. That doesn’t make the partner less abusive. Sending strength to CDC staff held hostage,” \u003Ca href=\"https://x.com/dr_demetre/status/1977342012752863483\"\u003Esaid Demetre Daskalakis\u003C/a\u003E, who served as the director of the National Center for Immunization and Respiratory Diseases, and was part of the wave of CDC leadership to resign earlier this year.\u003C/p\u003E \u003Cp\u003E“CDC damage is done. Rescinded firings or not. US health security is compromised,” he added.\u003C/p\u003E",
              "bodyTextSummary": "The firings of hundreds of employees at the Centers for Disease Control (CDC) have been reversed, according to several reports citing officials familiar with the matter, and the American Federation of Government Employees (AFGE), the largest union representing federal workers. On Friday, the White House budget office announced that as a result of the ongoing government shutdown, reductions in force (RIFs) across agencies have begun. A spokesperson for the Department of Health and Human Services (HHS), which houses the CDC, initially said that all employees that received layoff notices “were designated non-essential by their respective divisions”. However, over the weekend, the administration rescinded more than half of the 1,300 termination notices it sent to public health officials at the CDC, according to Axios and Reuters, citing sources familiar. Around 600 people at the agency remain fired. On Saturday, the New York Times reported that members of the Epidemic Intelligence Service (EIS), informally known as “disease detectives”, as well as the team that compiles the widely respected scientific journal, the Morbidity and Mortality Weekly Report, were among the employees reinstated. Initially, around 70 members of EIS were laid off, according to the Times report. Also affected were Athalia Christie and Maureen Bartee, who are leading the federal response to the measles outbreak. The Times reported that the two infectious disease experts were laid off, only to receive an email saying that their firings “on or about” 10 October had been rescinded a day later. A senior administration official told the Times that the mistakenly fired workers “were sent incorrect notifications”, adding that “any correction has already been remedied”. A federal health official also told ABC News that the mistake was due to a “coding error”. Neither the White House nor HHS have immediately responded to the Guardian’s requests for comment about how many employees have been recalled to their roles. “These firings are an assault on the health and lives of every person in the US,” said Gregg Gonsalves, an epidemiologist and member of Defend Public Health, a volunteer network of experts who work to challenge the Trump administration’s public health policies. “Did they not care enough to find out who they were firing and what they did before sending termination letters? The carelessness and callousness with which this administration handles life and death matters is unbelievable.” The AFGE has filed a lawsuit against the Trump administration, seeking to block the firings across agencies. In a court filing, the government said that the layoffs across the federal workforce will impact over 4,000 employees. Later this week, a federal judge in San Francisco will hear arguments in the case. The CDC has endured significant tumult in recent months. In August, a gunman targeted the agency’s headquarters in Atlanta, firing hundreds of bullets and killing a police officer in the attack. The perpetrator had blamed the Covid vaccine for making him depressed and suicidal. Health secretary Robert F Kennedy Jr then fired the recently appointed CDC director, Susan Monarez, after she spent less than a month on the job. Monarez’s removal has become an acrimonious flash point at the agency. At a Senate committee hearing, Monzarez said that Kennedy fired her for not complying with his vaccine agenda, adding that the health secretary had called the CDC the “most corrupt federal agency in the world”. Following her removal, several public health leaders left the agency in protest of political interference in their work. Debra Houry, the former chief medical officer at the CDC, said Kennedy “censored CDC science, politicized its processes and stripped leaders of independence” while speaking alongside Monarez on Capitol Hill last month. “Think about what it’s like to be at CDC. It’s like living with an abusive partner that attacks and then takes back some of the abuse. That doesn’t make the partner less abusive. Sending strength to CDC staff held hostage,” said Demetre Daskalakis, who served as the director of the National Center for Immunization and Respiratory Diseases, and was part of the wave of CDC leadership to resign earlier this year. “CDC damage is done. Rescinded firings or not. US health security is compromised,” he added.",
              "attributes": {

              },
              "published": True,
              "createdDate": "2025-10-13T15:48:51Z",
              "lastModifiedDate": "2025-10-13T15:42:02Z",
              "contributors": [],
              "elements": [
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003EThe firings of hundreds of employees at the Centers for Disease Control (CDC) have been reversed, according to several reports citing officials familiar with the matter, and the American Federation of Government Employees (AFGE), the largest union representing federal workers.\u003C/p\u003E \n\u003Cp\u003EOn Friday, the White House budget office \u003Ca href=\"https://www.theguardian.com/us-news/2025/oct/10/federal-workers-pay-government-shutdown\"\u003Eannounced\u003C/a\u003E that as a result of the ongoing government shutdown, reductions in force (RIFs) across agencies have begun.\u003C/p\u003E \n\u003Cp\u003EA spokesperson for the Department of Health and Human Services (HHS), which houses the CDC, initially said that all employees that received layoff notices “were designated non-essential by their respective divisions”.\u003C/p\u003E \n\u003Cp\u003EHowever, over the weekend, the administration rescinded more than half of the 1,300 termination notices it sent to public health officials at the CDC, according to \u003Ca href=\"https://www.axios.com/2025/10/13/trump-kennedy-cdc-firings-rehirings\"\u003EAxios\u003C/a\u003E and \u003Ca href=\"https://www.reuters.com/business/healthcare-pharmaceuticals/trump-administration-lays-off-dozens-cdc-officials-nyt-reports-2025-10-11/\"\u003EReuters\u003C/a\u003E, citing sources familiar. Around 600 people at the agency remain fired.\u003C/p\u003E \n\u003Cp\u003EOn Saturday, \u003Ca href=\"https://www.nytimes.com/2025/10/11/health/cdc-layoffs-measles.html\"\u003Ethe New York Times reported\u003C/a\u003E that members of the Epidemic Intelligence Service (EIS), informally known as “disease detectives”, as well as the team that compiles the widely respected scientific journal, the Morbidity and Mortality Weekly Report, were among the employees reinstated.\u003C/p\u003E \n\u003Cp\u003EInitially, around 70 members of EIS were laid off, according to the Times report. Also affected were Athalia Christie and Maureen Bartee, who are leading the federal response to the measles outbreak. The Times reported that the two infectious disease experts were laid off, only to receive an email saying that their firings “on or about” 10 October had been rescinded a day later.\u003C/p\u003E \n\u003Cp\u003EA senior administration official told the Times that the mistakenly fired workers “were sent incorrect notifications”, adding that “any correction has already been remedied”.\u003C/p\u003E \n\u003Cp\u003EA federal health official also \u003Ca href=\"https://abcnews.go.com/Politics/live-updates/government-shutdown-live-updates?id=126242587&amp;entryId=126436657&amp;userab=news_search_page_design_unification-429*variant_a_control_search-1786&amp;userab=news_search_page_design_unification-429*variant_b_search_redesign-1787\"\u003Etold ABC News\u003C/a\u003E that the mistake was due to a “coding error”. Neither the White House nor HHS have immediately responded to the Guardian’s requests for comment about how many employees have been recalled to their roles.\u003C/p\u003E \n\u003Cp\u003E“These firings are an assault on the health and lives of every person in the US,” said Gregg Gonsalves, an epidemiologist and member of Defend Public Health, a volunteer network of experts who work to challenge the Trump administration’s public health policies.\u003C/p\u003E \n\u003Cp\u003E“Did they not care enough to find out who they were firing and what they did before sending termination letters? The carelessness and callousness with which this administration handles life and death matters is unbelievable.”\u003C/p\u003E \n\u003Cp\u003EThe AFGE has filed a lawsuit against the Trump administration, seeking to block the firings across agencies. In a court filing, the government said that the layoffs across the federal workforce will impact over 4,000 employees. Later this week, a federal judge in San Francisco will hear arguments in the case.\u003C/p\u003E \n\u003Cp\u003EThe CDC has endured significant tumult in recent months. In August, a gunman targeted the agency’s headquarters in Atlanta, firing hundreds of bullets and killing a police officer in the attack. The perpetrator had blamed the Covid vaccine for making him depressed and suicidal.\u003C/p\u003E \n\u003Cp\u003EHealth secretary Robert F Kennedy Jr \u003Ca href=\"https://www.theguardian.com/us-news/2025/aug/28/rfk-resign-cdc-susan-monarez-fired\"\u003Ethen fired \u003C/a\u003Ethe recently appointed CDC director, Susan Monarez, after she spent less than a month on the job. Monarez’s removal has become an acrimonious flash point at the agency. At\u003Ca href=\"https://www.theguardian.com/us-news/2025/sep/17/cdc-director-susan-monarez-key-takeaways\"\u003E a Senate committee hearing\u003C/a\u003E, Monzarez said that Kennedy fired her for not complying with his vaccine agenda, adding that the health secretary had called the CDC the “most corrupt federal agency in the world”.\u003C/p\u003E \n\u003Cp\u003EFollowing her removal, several public health leaders \u003Ca href=\"https://www.theguardian.com/us-news/2025/aug/28/cdc-rally-staffers-protest\"\u003Eleft the agency\u003C/a\u003E in protest of political interference in their work. Debra Houry, the former chief medical officer at the CDC, said Kennedy “censored CDC science, politicized its processes and stripped leaders of independence” while speaking alongside Monarez on Capitol Hill last month.\u003C/p\u003E \n\u003Cp\u003E“Think about what it’s like to be at CDC. It’s like living with an abusive partner that attacks and then takes back some of the abuse. That doesn’t make the partner less abusive. Sending strength to CDC staff held hostage,” \u003Ca href=\"https://x.com/dr_demetre/status/1977342012752863483\"\u003Esaid Demetre Daskalakis\u003C/a\u003E, who served as the director of the National Center for Immunization and Respiratory Diseases, and was part of the wave of CDC leadership to resign earlier this year.\u003C/p\u003E \n\u003Cp\u003E“CDC damage is done. Rescinded firings or not. US health security is compromised,” he added.\u003C/p\u003E"
                  }
                }
              ]
            }
          ],
          "totalBodyBlocks": 1
        },
        "isHosted": False,
        "pillarId": "pillar/news",
        "pillarName": "News"
      }
    ]
  }
}


@pytest.fixture
def mock_guardian_api_multiple_responses():
    # simulates API query of keyword 'trump"
    return {
  "response": {
    "status": "ok",
    "userTier": "developer",
    "total": 292,
    "startIndex": 1,
    "pageSize": 2,
    "currentPage": 1,
    "pages": 146,
    "orderBy": "newest",
    "results": [
      {
        "id": "world/2025/oct/13/palestinian-prisoners-return-home",
        "type": "article",
        "sectionId": "world",
        "sectionName": "World news",
        "webPublicationDate": "2025-10-13T15:18:21Z",
        "webTitle": "‘Locked up for 24 years’: joy and sorrow as Palestinian prisoners and detainees return home",
        "webUrl": "https://www.theguardian.com/world/2025/oct/13/palestinian-prisoners-return-home",
        "apiUrl": "https://content.guardianapis.com/world/2025/oct/13/palestinian-prisoners-return-home",
        "blocks": {
          "body": [
            {
              "id": "68ed05938f08f99dceddd8d0",
              "bodyHtml": "\u003Cp\u003EThe police could not hold the crowds back. As soon as they saw the Palestinian prisoners through the windows of the bus, hundreds of people gathering in front of a theatre in Ramallah in the occupied West Bank rushed forward, chanting the names of loved ones they had not seen for years and in some cases, decades.\u003C/p\u003E \u003Cp\u003EThe prisoners were gaunt, the sharp angles of their faces decorated by freshly scabbed-over wounds. Loved ones hoisted them up on their shoulders with ease. One prisoner, swaddled in a Palestinian keffiyeh and splaying his fingers into a V for victory, was dropped before his mother, whose feet he began to kiss.\u003C/p\u003E    \u003Cp\u003EIn total, 88 Palestinians were released from Israeli prisons and sent to the occupied West Bank on Monday – the other nearly 2,000, a number that includes about 1,700 Palestinians seized from Gaza during the war and held without charge, were sent back to Gaza, where a minority would travel on to neighbouring countries.\u003C/p\u003E \u003Cp\u003EThe detainees and prisoners were released by Israel a few hours after all living Israeli hostages were returned from Gaza. The exchange marked the \u003Ca href=\"https://www.theguardian.com/world/2025/oct/09/first-phase-of-ceasefire-deal-to-end-war-in-gaza-agreed-by-israel-and-hamas\"\u003Efirst step in a ceasefire\u003C/a\u003E that could permanently end the two-year conflict in the territory.\u003C/p\u003E    \u003Cp\u003EThe geopolitical implication of the release was far from families’ minds in Ramallah on Monday; most were celebrating a release they never thought would come. Most of the men returning to the West Bank were serving life sentences and many were charged with violent crimes.\u003C/p\u003E \u003Cp\u003E“He’s been locked up for 24 years,” said a relative of Saber Masalma, a member of Fatah, the main faction of the Palestine Liberation Organization (PLO) who was arrested in 2002 and sentenced to life in prison on charges of conspiracy to cause death and placing explosive charges.\u003C/p\u003E \u003Cp\u003EHe shoved a phone in Masalma’s face, eager to introduce him to his adult niece over a video call, while he juggled requests for selfies with his relatives.\u003C/p\u003E \u003Cp\u003EHe had not seen Masalma for two years, as Israel had cut off family visits to detainees after the 7 October attack by Hamas-led militants who killed about 1,200 people and took 251 hostage. Masalma had warned him over the phone that he might not recognise him owing to the amount of weight he had lost in prison.\u003C/p\u003E \u003Cp\u003E“He looks like a dead body. But we will bring him back to life,” he said, laughing. They were off to a restaurant, where they would have to be careful that Saber did not eat too much, as his stomach was not used to much food after not eating well in prison.\u003C/p\u003E    \u003Cp\u003EThe other prisoners also looked to be in bad shape. Their cheekbones jutted out, with some bearing the marks of recent beatings and a few unable to walk without being propped up by their relatives.\u003Cbr\u003E\u003Cbr\u003EWhen asked about their treatment in the prisons, a detainee apologised to the Guardian and said he could not answer, for fear that he would face repercussions from Israeli authorities, only saying that it was “horrible”.\u003C/p\u003E \u003Cp\u003EAnother prisoner said that the conditions were “very, very, very difficult,” and that the last two years in prison were the “worst two years of his life”, asking that he not be named.\u003C/p\u003E \u003Cp\u003EPrior to Monday’s release, 11,056 Palestinians were held in Israeli prisons, according to statistics from the Israeli NGO HaMoked in October 2025. At least 3,500 of those were held in administrative detention without trial.\u003C/p\u003E \u003Cp\u003EPalestinians have faced abuse and inhumane treatment in Israeli prisons “as a matter of policy” according to the Israeli human rights organisation B’Tselem. The group alleges that Palestinian prisoners are denied medical treatment, adequate food and face physical abuse in Israeli prisons.\u003C/p\u003E    \u003Cp\u003EActivists have long said that wide-scale imprisonment of Palestinians is used as a tool to enforce Israel’s occupation of the Palestinian territories, with statistics estimating up to 40% of Palestinians have been arrested at some point. \u003Cbr\u003E\u003Cbr\u003EIsrael says that its prison system complies with international law.\u003C/p\u003E \u003Cp\u003EIsrael also forbade people from celebrating the prisoners’ release on Monday, firing teargas at family members and journalists waiting near Ofer prison, in the occupied West Bank, where detainees were kept. A flyer distributed by the Israeli military warned people that “we are surveilling you everywhere” and threatening that if they supported “terrorist organisations” they could be arrested.\u003C/p\u003E \u003Cp\u003EThe Guardian spoke with six different relatives of prisoners who said they were visited by Israeli security services in recent days.\u003C/p\u003E \u003Cp\u003E“They came to warn us not to hold celebrations, not to raise flags or banners, not to gather in the diwan [hall]. These days, the hardest thing is to speak the truth,” said a relative of the prisoner Hani al-Zeer, who asked not to be identified by name out of fear of security repercussions. Al-Zeer had been imprisoned for 23 years, and the relative, as well as al-Zeer’s son, had also been imprisoned several times.\u003C/p\u003E    \u003Cp\u003EAmid the scenes of joy, there was also sorrow. Several families who had been told by the Israeli security services that their family members would be returning home were surprised to see that they were not on the buses on Monday.\u003C/p\u003E \u003Cp\u003ETwo different prisoner lists were circulating on Monday morning in the hours before prisoners were released. On one list, some prisoners were slated to be released back home, on the other, prisoners were to be deported to Gaza. \u003Cbr\u003E\u003Cbr\u003ETo Um Abed, whose brother had been scheduled for release, the sudden possibility that her brother, Kamal Imran, could be deported to Gaza, came as a shock. If he was deported to Gaza, there was virtually no way for her to see him unless he was able to leave the territory.\u003C/p\u003E \u003Caside class=\"element element-rich-link element--thumbnail\"\u003E \u003Cp\u003E \u003Cspan\u003ERelated: \u003C/span\u003E\u003Ca href=\"https://www.theguardian.com/world/2025/oct/13/hamas-deploys-armed-fighters-and-police-across-parts-of-gaza\"\u003EHamas deploys armed fighters and police across parts of Gaza\u003C/a\u003E \u003C/p\u003E \u003C/aside\u003E  \u003Cp\u003E“We’ve been waiting here for his release for two days. We’re shocked to hear this. The Israelis stormed our house and told us we were forbidden from doing any kind of celebration – so he should be released,” said Um Abed, tears in her eyes.\u003C/p\u003E \u003Cp\u003EShe waited anxiously as the buses arrived to the drop-off point in Ramallah, waiting for her brother to emerge. When the last man got off the buses with no sign of her brother, she clutched her cheeks and wailed.\u003C/p\u003E \u003Cp\u003EOthers evidently had been told their loved ones were to be returned home, only to find out at the last minute that they were being deported. “Why are they deporting him?” a woman screamed in tears, as police officers rushed her away from the crowd.\u003C/p\u003E \u003Cp\u003E“It would have been easier if they just told us from the beginning. We don’t know where he is. Egypt? Gaza? We are devastated,” said Raed Imran, as he led Abed to the car where she had been preparing to receive her brother.\u003C/p\u003E",
              "bodyTextSummary": "The police could not hold the crowds back. As soon as they saw the Palestinian prisoners through the windows of the bus, hundreds of people gathering in front of a theatre in Ramallah in the occupied West Bank rushed forward, chanting the names of loved ones they had not seen for years and in some cases, decades. The prisoners were gaunt, the sharp angles of their faces decorated by freshly scabbed-over wounds. Loved ones hoisted them up on their shoulders with ease. One prisoner, swaddled in a Palestinian keffiyeh and splaying his fingers into a V for victory, was dropped before his mother, whose feet he began to kiss.\nIn total, 88 Palestinians were released from Israeli prisons and sent to the occupied West Bank on Monday – the other nearly 2,000, a number that includes about 1,700 Palestinians seized from Gaza during the war and held without charge, were sent back to Gaza, where a minority would travel on to neighbouring countries. The detainees and prisoners were released by Israel a few hours after all living Israeli hostages were returned from Gaza. The exchange marked the first step in a ceasefire that could permanently end the two-year conflict in the territory.\nThe geopolitical implication of the release was far from families’ minds in Ramallah on Monday; most were celebrating a release they never thought would come. Most of the men returning to the West Bank were serving life sentences and many were charged with violent crimes. “He’s been locked up for 24 years,” said a relative of Saber Masalma, a member of Fatah, the main faction of the Palestine Liberation Organization (PLO) who was arrested in 2002 and sentenced to life in prison on charges of conspiracy to cause death and placing explosive charges. He shoved a phone in Masalma’s face, eager to introduce him to his adult niece over a video call, while he juggled requests for selfies with his relatives. He had not seen Masalma for two years, as Israel had cut off family visits to detainees after the 7 October attack by Hamas-led militants who killed about 1,200 people and took 251 hostage. Masalma had warned him over the phone that he might not recognise him owing to the amount of weight he had lost in prison. “He looks like a dead body. But we will bring him back to life,” he said, laughing. They were off to a restaurant, where they would have to be careful that Saber did not eat too much, as his stomach was not used to much food after not eating well in prison.\nThe other prisoners also looked to be in bad shape. Their cheekbones jutted out, with some bearing the marks of recent beatings and a few unable to walk without being propped up by their relatives. When asked about their treatment in the prisons, a detainee apologised to the Guardian and said he could not answer, for fear that he would face repercussions from Israeli authorities, only saying that it was “horrible”. Another prisoner said that the conditions were “very, very, very difficult,” and that the last two years in prison were the “worst two years of his life”, asking that he not be named. Prior to Monday’s release, 11,056 Palestinians were held in Israeli prisons, according to statistics from the Israeli NGO HaMoked in October 2025. At least 3,500 of those were held in administrative detention without trial. Palestinians have faced abuse and inhumane treatment in Israeli prisons “as a matter of policy” according to the Israeli human rights organisation B’Tselem. The group alleges that Palestinian prisoners are denied medical treatment, adequate food and face physical abuse in Israeli prisons.\nActivists have long said that wide-scale imprisonment of Palestinians is used as a tool to enforce Israel’s occupation of the Palestinian territories, with statistics estimating up to 40% of Palestinians have been arrested at some point. Israel says that its prison system complies with international law. Israel also forbade people from celebrating the prisoners’ release on Monday, firing teargas at family members and journalists waiting near Ofer prison, in the occupied West Bank, where detainees were kept. A flyer distributed by the Israeli military warned people that “we are surveilling you everywhere” and threatening that if they supported “terrorist organisations” they could be arrested. The Guardian spoke with six different relatives of prisoners who said they were visited by Israeli security services in recent days. “They came to warn us not to hold celebrations, not to raise flags or banners, not to gather in the diwan [hall]. These days, the hardest thing is to speak the truth,” said a relative of the prisoner Hani al-Zeer, who asked not to be identified by name out of fear of security repercussions. Al-Zeer had been imprisoned for 23 years, and the relative, as well as al-Zeer’s son, had also been imprisoned several times.\nAmid the scenes of joy, there was also sorrow. Several families who had been told by the Israeli security services that their family members would be returning home were surprised to see that they were not on the buses on Monday. Two different prisoner lists were circulating on Monday morning in the hours before prisoners were released. On one list, some prisoners were slated to be released back home, on the other, prisoners were to be deported to Gaza. To Um Abed, whose brother had been scheduled for release, the sudden possibility that her brother, Kamal Imran, could be deported to Gaza, came as a shock. If he was deported to Gaza, there was virtually no way for her to see him unless he was able to leave the territory.\n“We’ve been waiting here for his release for two days. We’re shocked to hear this. The Israelis stormed our house and told us we were forbidden from doing any kind of celebration – so he should be released,” said Um Abed, tears in her eyes. She waited anxiously as the buses arrived to the drop-off point in Ramallah, waiting for her brother to emerge. When the last man got off the buses with no sign of her brother, she clutched her cheeks and wailed. Others evidently had been told their loved ones were to be returned home, only to find out at the last minute that they were being deported. “Why are they deporting him?” a woman screamed in tears, as police officers rushed her away from the crowd. “It would have been easier if they just told us from the beginning. We don’t know where he is. Egypt? Gaza? We are devastated,” said Raed Imran, as he led Abed to the car where she had been preparing to receive her brother.",
              "attributes": {

              },
              "published": True,
              "createdDate": "2025-10-13T15:18:21Z",
              "firstPublishedDate": "2025-10-13T15:27:08Z",
              "publishedDate": "2025-10-13T15:41:23Z",
              "lastModifiedDate": "2025-10-13T15:41:23Z",
              "contributors": [],
              "elements": [
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003EThe police could not hold the crowds back. As soon as they saw the Palestinian prisoners through the windows of the bus, hundreds of people gathering in front of a theatre in Ramallah in the occupied West Bank rushed forward, chanting the names of loved ones they had not seen for years and in some cases, decades.\u003C/p\u003E \n\u003Cp\u003EThe prisoners were gaunt, the sharp angles of their faces decorated by freshly scabbed-over wounds. Loved ones hoisted them up on their shoulders with ease. One prisoner, swaddled in a Palestinian keffiyeh and splaying his fingers into a V for victory, was dropped before his mother, whose feet he began to kiss.\u003C/p\u003E"
                  }
                },
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003EIn total, 88 Palestinians were released from Israeli prisons and sent to the occupied West Bank on Monday – the other nearly 2,000, a number that includes about 1,700 Palestinians seized from Gaza during the war and held without charge, were sent back to Gaza, where a minority would travel on to neighbouring countries.\u003C/p\u003E \n\u003Cp\u003EThe detainees and prisoners were released by Israel a few hours after all living Israeli hostages were returned from Gaza. The exchange marked the \u003Ca href=\"https://www.theguardian.com/world/2025/oct/09/first-phase-of-ceasefire-deal-to-end-war-in-gaza-agreed-by-israel-and-hamas\"\u003Efirst step in a ceasefire\u003C/a\u003E that could permanently end the two-year conflict in the territory.\u003C/p\u003E"
                  }
                },
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003EThe geopolitical implication of the release was far from families’ minds in Ramallah on Monday; most were celebrating a release they never thought would come. Most of the men returning to the West Bank were serving life sentences and many were charged with violent crimes.\u003C/p\u003E \n\u003Cp\u003E“He’s been locked up for 24 years,” said a relative of Saber Masalma, a member of Fatah, the main faction of the Palestine Liberation Organization (PLO) who was arrested in 2002 and sentenced to life in prison on charges of conspiracy to cause death and placing explosive charges.\u003C/p\u003E \n\u003Cp\u003EHe shoved a phone in Masalma’s face, eager to introduce him to his adult niece over a video call, while he juggled requests for selfies with his relatives.\u003C/p\u003E \n\u003Cp\u003EHe had not seen Masalma for two years, as Israel had cut off family visits to detainees after the 7 October attack by Hamas-led militants who killed about 1,200 people and took 251 hostage. Masalma had warned him over the phone that he might not recognise him owing to the amount of weight he had lost in prison.\u003C/p\u003E \n\u003Cp\u003E“He looks like a dead body. But we will bring him back to life,” he said, laughing. They were off to a restaurant, where they would have to be careful that Saber did not eat too much, as his stomach was not used to much food after not eating well in prison.\u003C/p\u003E"
                  }
                },
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003EThe other prisoners also looked to be in bad shape. Their cheekbones jutted out, with some bearing the marks of recent beatings and a few unable to walk without being propped up by their relatives.\u003Cbr\u003E\u003Cbr\u003EWhen asked about their treatment in the prisons, a detainee apologised to the Guardian and said he could not answer, for fear that he would face repercussions from Israeli authorities, only saying that it was “horrible”.\u003C/p\u003E \n\u003Cp\u003EAnother prisoner said that the conditions were “very, very, very difficult,” and that the last two years in prison were the “worst two years of his life”, asking that he not be named.\u003C/p\u003E \n\u003Cp\u003EPrior to Monday’s release, 11,056 Palestinians were held in Israeli prisons, according to statistics from the Israeli NGO HaMoked in October 2025. At least 3,500 of those were held in administrative detention without trial.\u003C/p\u003E \n\u003Cp\u003EPalestinians have faced abuse and inhumane treatment in Israeli prisons “as a matter of policy” according to the Israeli human rights organisation B’Tselem. The group alleges that Palestinian prisoners are denied medical treatment, adequate food and face physical abuse in Israeli prisons.\u003C/p\u003E"
                  }
                },
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003EActivists have long said that wide-scale imprisonment of Palestinians is used as a tool to enforce Israel’s occupation of the Palestinian territories, with statistics estimating up to 40% of Palestinians have been arrested at some point. \u003Cbr\u003E\u003Cbr\u003EIsrael says that its prison system complies with international law.\u003C/p\u003E \n\u003Cp\u003EIsrael also forbade people from celebrating the prisoners’ release on Monday, firing teargas at family members and journalists waiting near Ofer prison, in the occupied West Bank, where detainees were kept. A flyer distributed by the Israeli military warned people that “we are surveilling you everywhere” and threatening that if they supported “terrorist organisations” they could be arrested.\u003C/p\u003E \n\u003Cp\u003EThe Guardian spoke with six different relatives of prisoners who said they were visited by Israeli security services in recent days.\u003C/p\u003E \n\u003Cp\u003E“They came to warn us not to hold celebrations, not to raise flags or banners, not to gather in the diwan [hall]. These days, the hardest thing is to speak the truth,” said a relative of the prisoner Hani al-Zeer, who asked not to be identified by name out of fear of security repercussions. Al-Zeer had been imprisoned for 23 years, and the relative, as well as al-Zeer’s son, had also been imprisoned several times.\u003C/p\u003E"
                  }
                },
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003EAmid the scenes of joy, there was also sorrow. Several families who had been told by the Israeli security services that their family members would be returning home were surprised to see that they were not on the buses on Monday.\u003C/p\u003E \n\u003Cp\u003ETwo different prisoner lists were circulating on Monday morning in the hours before prisoners were released. On one list, some prisoners were slated to be released back home, on the other, prisoners were to be deported to Gaza. \u003Cbr\u003E\u003Cbr\u003ETo Um Abed, whose brother had been scheduled for release, the sudden possibility that her brother, Kamal Imran, could be deported to Gaza, came as a shock. If he was deported to Gaza, there was virtually no way for her to see him unless he was able to leave the territory.\u003C/p\u003E"
                  }
                },
                {
                  "type": "rich-link",
                  "assets": [],
                  "richLinkTypeData": {
                    "url": "https://www.theguardian.com/world/2025/oct/13/hamas-deploys-armed-fighters-and-police-across-parts-of-gaza",
                    "originalUrl": "https://www.theguardian.com/world/2025/oct/13/hamas-deploys-armed-fighters-and-police-across-parts-of-gaza",
                    "linkText": "Hamas deploys armed fighters and police across parts of Gaza",
                    "linkPrefix": "Related: ",
                    "role": "thumbnail"
                  }
                },
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003E“We’ve been waiting here for his release for two days. We’re shocked to hear this. The Israelis stormed our house and told us we were forbidden from doing any kind of celebration – so he should be released,” said Um Abed, tears in her eyes.\u003C/p\u003E \n\u003Cp\u003EShe waited anxiously as the buses arrived to the drop-off point in Ramallah, waiting for her brother to emerge. When the last man got off the buses with no sign of her brother, she clutched her cheeks and wailed.\u003C/p\u003E \n\u003Cp\u003EOthers evidently had been told their loved ones were to be returned home, only to find out at the last minute that they were being deported. “Why are they deporting him?” a woman screamed in tears, as police officers rushed her away from the crowd.\u003C/p\u003E \n\u003Cp\u003E“It would have been easier if they just told us from the beginning. We don’t know where he is. Egypt? Gaza? We are devastated,” said Raed Imran, as he led Abed to the car where she had been preparing to receive her brother.\u003C/p\u003E"
                  }
                }
              ]
            }
          ],
          "totalBodyBlocks": 1
        },
        "isHosted": False,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "world/2025/oct/13/why-us-china-trade-war-restarted-tariffs",
        "type": "article",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-10-13T14:16:56Z",
        "webTitle": "Why has the US-China trade war restarted and how have markets reacted?",
        "webUrl": "https://www.theguardian.com/world/2025/oct/13/why-us-china-trade-war-restarted-tariffs",
        "apiUrl": "https://content.guardianapis.com/world/2025/oct/13/why-us-china-trade-war-restarted-tariffs",
        "blocks": {
          "body": [
            {
              "id": "68eccde88f085c374050c5cf",
              "bodyHtml": "\u003Cp\u003EWith nearly a month to go before the deadline for the US and China to reach a deal in their trade war, goodwill between the two countries appears to have been swept off the table in recent days. China announced that it was once again \u003Ca href=\"https://www.theguardian.com/world/2025/oct/09/china-steps-up-control-rare-earth-exports-national-security-concerns\"\u003Erestricting the export of critical minerals\u003C/a\u003E, prompting the US president, Donald Trump, to announce \u003Ca href=\"https://www.theguardian.com/us-news/2025/oct/12/china-warns-us-of-retaliation-over-trump-100-tariffs-threat\"\u003Etariffs of 100%\u003C/a\u003E on US-bound Chinese exports, scuppering, at least for now, hopes that global economic turmoil could be averted.\u003C/p\u003E \u003Ch2\u003EWhy has the US-China trade war restarted?\u003C/h2\u003E \u003Cp\u003EOn Thursday, China’s commerce ministry announced enhanced restrictions on the \u003Ca href=\"https://www.theguardian.com/world/2025/oct/09/china-steps-up-control-rare-earth-exports-national-security-concerns\"\u003Eexport of rare earths\u003C/a\u003E, citing national security concerns.\u003C/p\u003E \u003Cp\u003EChina’s chokehold on the global supply chain of rare earths – minerals found in the Earth’s crust that are used to make everything from consumer electronics to cars to military equipment – has been a sticking point in the trade war. China produces more than 90% of the world’s processed rare earths and \u003Ca href=\"https://www.theguardian.com/world/2025/jun/26/china-rare-earths-baotou-life-metallic-elements\"\u003Econtrols about 70% of the world’s mining\u003C/a\u003E.\u003C/p\u003E \u003Cp\u003ETrump responded by calling China’s decision “extremely hostile” and announcing across the board tariffs of 100% on Chinese imports.\u003C/p\u003E \u003Cp\u003EAs of 25 September, average US tariffs on Chinese imports reached 58%, while Chinese tariffs reached 33%, according to analysis by the Peterson Institute for International Economics. Higher tariffs reaching nearly 150% have been threatened but are on pause before a 10 November deadline to reach a deal.\u003C/p\u003E \u003Cp\u003EChina’s rare earths announcement did not come out of the blue. Last month, the US announced enhanced controls on the export of chipmaking equipment to China, aimed at closing perceived loopholes in Washington’s plans to deprive China of advanced semiconductors.\u003C/p\u003E \u003Cp\u003EThis is not the first time that Beijing has exploited its control of rare earths. In April, \u003Ca href=\"https://www.theguardian.com/us-news/2025/apr/16/china-trade-war-us-arms-firms-rare-earths-supply\"\u003Eexports were restricted\u003C/a\u003E, causing manufacturing slowdowns around the world. It temporarily lifted those restrictions a few months later.\u003C/p\u003E \u003Cp\u003E“Beijing is effectively reactivating its April playbook – escalating first to force a negotiation reset, rather than waiting passively for the next talks,” said Hutong Research, an independent advisory firm based in Beijing and Shanghai.\u003C/p\u003E \u003Ch2\u003EWhat progress had been made in recent months?\u003C/h2\u003E \u003Cp\u003EThe return of hostilities comes after there had been some signs of thawing on both sides.\u003C/p\u003E \u003Cp\u003EIn September, the US and China reached \u003Ca href=\"https://www.theguardian.com/technology/2025/sep/25/trump-china-tiktok-deal\"\u003Ea deal on TikTok\u003C/a\u003E, the Chinese-owned social media app that faced being banned in the US if its parent company, ByteDance, did not divest. After talks in Madrid, Beijing and Washington agreed to a deal in which the platform would switch to US-controlled ownership. China called the agreement a “win-win”. Trump and Xi Jinping, China’s president, \u003Ca href=\"https://www.theguardian.com/technology/2025/sep/19/deal-to-transfer-tiktok-to-us-control-unresolved-trump-xi-call\"\u003Espoke on the phone\u003C/a\u003E that week to confirm the deal.\u003C/p\u003E \u003Cp\u003ENews of the deal was followed by a group of US lawmakers visiting China for the first time since 2019. They met China’s premier, Li Qiang, and talked of the need to “break the ice”.\u003C/p\u003E \u003Cp\u003EBut it has not all been plain sailing. As well as disagreements over access to chipmaking equipment, the US and China have been at loggerheads over China’s purchases of Russian oil and declining soya bean exports from the US to China. Since Trump’s first trade war in 2018, \u003Ca href=\"https://www.theguardian.com/world/2025/may/24/as-trump-focuses-on-his-trade-war-brazil-and-china-forge-closer-ties\"\u003EChina has reduced its reliance on the US for key commodities\u003C/a\u003E.\u003C/p\u003E \u003Ch2\u003EWill Trump and Xi meet to negotiate a new deal?\u003C/h2\u003E \u003Cp\u003ETrump and Xi were expected to meet at the Apec summit in South Korea, which starts at the end of this month. There was also talk of Trump visiting Beijing in January. Those meetings seem less probable now.\u003C/p\u003E \u003Cp\u003E“I was to meet President Xi in two weeks, at Apec, in South Korea, but now there seems to be no reason to do so,” Trump wrote on the social media platform Truth Social on Friday.\u003C/p\u003E \u003Ch2\u003EHow have the markets reacted?\u003C/h2\u003E \u003Cp\u003EUS markets initially panicked on the news. But on Sunday, Trump appeared to \u003Ca href=\"https://www.theguardian.com/business/2025/oct/13/markets-rebound-us-china-tariff-taco-trade\"\u003Esoften his tone\u003C/a\u003E towards Xi, writing on Truth Social that “it will all be fine” and that “the USA wants to help China, not hurt it!!!”, which prompted a rebound. Analysts speculated that markets may rally because of hopes of a “Taco trade” – an acronym for “Trump always chickens out”.\u003C/p\u003E \u003Cp\u003EBut all eyes will now be on Beijing to see if it imposes counter-tariffs. On Sunday, the commerce ministry \u003Ca href=\"https://www.theguardian.com/us-news/2025/oct/12/china-warns-us-of-retaliation-over-trump-100-tariffs-threat\"\u003Esaid\u003C/a\u003E China would pursue “resolute measures to protect its legitimate rights and interests”. China may also renege on the TikTok deal, which could do more political damage than tit-for-tat tariffs.\u003C/p\u003E",
              "bodyTextSummary": "With nearly a month to go before the deadline for the US and China to reach a deal in their trade war, goodwill between the two countries appears to have been swept off the table in recent days. China announced that it was once again restricting the export of critical minerals, prompting the US president, Donald Trump, to announce tariffs of 100% on US-bound Chinese exports, scuppering, at least for now, hopes that global economic turmoil could be averted. Why has the US-China trade war restarted? On Thursday, China’s commerce ministry announced enhanced restrictions on the export of rare earths, citing national security concerns. China’s chokehold on the global supply chain of rare earths – minerals found in the Earth’s crust that are used to make everything from consumer electronics to cars to military equipment – has been a sticking point in the trade war. China produces more than 90% of the world’s processed rare earths and controls about 70% of the world’s mining. Trump responded by calling China’s decision “extremely hostile” and announcing across the board tariffs of 100% on Chinese imports. As of 25 September, average US tariffs on Chinese imports reached 58%, while Chinese tariffs reached 33%, according to analysis by the Peterson Institute for International Economics. Higher tariffs reaching nearly 150% have been threatened but are on pause before a 10 November deadline to reach a deal. China’s rare earths announcement did not come out of the blue. Last month, the US announced enhanced controls on the export of chipmaking equipment to China, aimed at closing perceived loopholes in Washington’s plans to deprive China of advanced semiconductors. This is not the first time that Beijing has exploited its control of rare earths. In April, exports were restricted, causing manufacturing slowdowns around the world. It temporarily lifted those restrictions a few months later. “Beijing is effectively reactivating its April playbook – escalating first to force a negotiation reset, rather than waiting passively for the next talks,” said Hutong Research, an independent advisory firm based in Beijing and Shanghai. What progress had been made in recent months? The return of hostilities comes after there had been some signs of thawing on both sides. In September, the US and China reached a deal on TikTok, the Chinese-owned social media app that faced being banned in the US if its parent company, ByteDance, did not divest. After talks in Madrid, Beijing and Washington agreed to a deal in which the platform would switch to US-controlled ownership. China called the agreement a “win-win”. Trump and Xi Jinping, China’s president, spoke on the phone that week to confirm the deal. News of the deal was followed by a group of US lawmakers visiting China for the first time since 2019. They met China’s premier, Li Qiang, and talked of the need to “break the ice”. But it has not all been plain sailing. As well as disagreements over access to chipmaking equipment, the US and China have been at loggerheads over China’s purchases of Russian oil and declining soya bean exports from the US to China. Since Trump’s first trade war in 2018, China has reduced its reliance on the US for key commodities. Will Trump and Xi meet to negotiate a new deal? Trump and Xi were expected to meet at the Apec summit in South Korea, which starts at the end of this month. There was also talk of Trump visiting Beijing in January. Those meetings seem less probable now. “I was to meet President Xi in two weeks, at Apec, in South Korea, but now there seems to be no reason to do so,” Trump wrote on the social media platform Truth Social on Friday. How have the markets reacted? US markets initially panicked on the news. But on Sunday, Trump appeared to soften his tone towards Xi, writing on Truth Social that “it will all be fine” and that “the USA wants to help China, not hurt it!!!”, which prompted a rebound. Analysts speculated that markets may rally because of hopes of a “Taco trade” – an acronym for “Trump always chickens out”. But all eyes will now be on Beijing to see if it imposes counter-tariffs. On Sunday, the commerce ministry said China would pursue “resolute measures to protect its legitimate rights and interests”. China may also renege on the TikTok deal, which could do more political damage than tit-for-tat tariffs.",
              "attributes": {

              },
              "published": True,
              "createdDate": "2025-10-13T13:17:02Z",
              "firstPublishedDate": "2025-10-13T14:16:41Z",
              "publishedDate": "2025-10-13T15:33:09Z",
              "lastModifiedDate": "2025-10-13T15:33:09Z",
              "contributors": [],
              "elements": [
                {
                  "type": "text",
                  "assets": [],
                  "textTypeData": {
                    "html": "\u003Cp\u003EWith nearly a month to go before the deadline for the US and China to reach a deal in their trade war, goodwill between the two countries appears to have been swept off the table in recent days. China announced that it was once again \u003Ca href=\"https://www.theguardian.com/world/2025/oct/09/china-steps-up-control-rare-earth-exports-national-security-concerns\"\u003Erestricting the export of critical minerals\u003C/a\u003E, prompting the US president, Donald Trump, to announce \u003Ca href=\"https://www.theguardian.com/us-news/2025/oct/12/china-warns-us-of-retaliation-over-trump-100-tariffs-threat\"\u003Etariffs of 100%\u003C/a\u003E on US-bound Chinese exports, scuppering, at least for now, hopes that global economic turmoil could be averted.\u003C/p\u003E \n\u003Ch2\u003EWhy has the US-China trade war restarted?\u003C/h2\u003E \n\u003Cp\u003EOn Thursday, China’s commerce ministry announced enhanced restrictions on the \u003Ca href=\"https://www.theguardian.com/world/2025/oct/09/china-steps-up-control-rare-earth-exports-national-security-concerns\"\u003Eexport of rare earths\u003C/a\u003E, citing national security concerns.\u003C/p\u003E \n\u003Cp\u003EChina’s chokehold on the global supply chain of rare earths – minerals found in the Earth’s crust that are used to make everything from consumer electronics to cars to military equipment – has been a sticking point in the trade war. China produces more than 90% of the world’s processed rare earths and \u003Ca href=\"https://www.theguardian.com/world/2025/jun/26/china-rare-earths-baotou-life-metallic-elements\"\u003Econtrols about 70% of the world’s mining\u003C/a\u003E.\u003C/p\u003E \n\u003Cp\u003ETrump responded by calling China’s decision “extremely hostile” and announcing across the board tariffs of 100% on Chinese imports.\u003C/p\u003E \n\u003Cp\u003EAs of 25 September, average US tariffs on Chinese imports reached 58%, while Chinese tariffs reached 33%, according to analysis by the Peterson Institute for International Economics. Higher tariffs reaching nearly 150% have been threatened but are on pause before a 10 November deadline to reach a deal.\u003C/p\u003E \n\u003Cp\u003EChina’s rare earths announcement did not come out of the blue. Last month, the US announced enhanced controls on the export of chipmaking equipment to China, aimed at closing perceived loopholes in Washington’s plans to deprive China of advanced semiconductors.\u003C/p\u003E \n\u003Cp\u003EThis is not the first time that Beijing has exploited its control of rare earths. In April, \u003Ca href=\"https://www.theguardian.com/us-news/2025/apr/16/china-trade-war-us-arms-firms-rare-earths-supply\"\u003Eexports were restricted\u003C/a\u003E, causing manufacturing slowdowns around the world. It temporarily lifted those restrictions a few months later.\u003C/p\u003E \n\u003Cp\u003E“Beijing is effectively reactivating its April playbook – escalating first to force a negotiation reset, rather than waiting passively for the next talks,” said Hutong Research, an independent advisory firm based in Beijing and Shanghai.\u003C/p\u003E \n\u003Ch2\u003EWhat progress had been made in recent months?\u003C/h2\u003E \n\u003Cp\u003EThe return of hostilities comes after there had been some signs of thawing on both sides.\u003C/p\u003E \n\u003Cp\u003EIn September, the US and China reached \u003Ca href=\"https://www.theguardian.com/technology/2025/sep/25/trump-china-tiktok-deal\"\u003Ea deal on TikTok\u003C/a\u003E, the Chinese-owned social media app that faced being banned in the US if its parent company, ByteDance, did not divest. After talks in Madrid, Beijing and Washington agreed to a deal in which the platform would switch to US-controlled ownership. China called the agreement a “win-win”. Trump and Xi Jinping, China’s president, \u003Ca href=\"https://www.theguardian.com/technology/2025/sep/19/deal-to-transfer-tiktok-to-us-control-unresolved-trump-xi-call\"\u003Espoke on the phone\u003C/a\u003E that week to confirm the deal.\u003C/p\u003E \n\u003Cp\u003ENews of the deal was followed by a group of US lawmakers visiting China for the first time since 2019. They met China’s premier, Li Qiang, and talked of the need to “break the ice”.\u003C/p\u003E \n\u003Cp\u003EBut it has not all been plain sailing. As well as disagreements over access to chipmaking equipment, the US and China have been at loggerheads over China’s purchases of Russian oil and declining soya bean exports from the US to China. Since Trump’s first trade war in 2018, \u003Ca href=\"https://www.theguardian.com/world/2025/may/24/as-trump-focuses-on-his-trade-war-brazil-and-china-forge-closer-ties\"\u003EChina has reduced its reliance on the US for key commodities\u003C/a\u003E.\u003C/p\u003E \n\u003Ch2\u003EWill Trump and Xi meet to negotiate a new deal?\u003C/h2\u003E \n\u003Cp\u003ETrump and Xi were expected to meet at the Apec summit in South Korea, which starts at the end of this month. There was also talk of Trump visiting Beijing in January. Those meetings seem less probable now.\u003C/p\u003E \n\u003Cp\u003E“I was to meet President Xi in two weeks, at Apec, in South Korea, but now there seems to be no reason to do so,” Trump wrote on the social media platform Truth Social on Friday.\u003C/p\u003E \n\u003Ch2\u003EHow have the markets reacted?\u003C/h2\u003E \n\u003Cp\u003EUS markets initially panicked on the news. But on Sunday, Trump appeared to \u003Ca href=\"https://www.theguardian.com/business/2025/oct/13/markets-rebound-us-china-tariff-taco-trade\"\u003Esoften his tone\u003C/a\u003E towards Xi, writing on Truth Social that “it will all be fine” and that “the USA wants to help China, not hurt it!!!”, which prompted a rebound. Analysts speculated that markets may rally because of hopes of a “Taco trade” – an acronym for “Trump always chickens out”.\u003C/p\u003E \n\u003Cp\u003EBut all eyes will now be on Beijing to see if it imposes counter-tariffs. On Sunday, the commerce ministry \u003Ca href=\"https://www.theguardian.com/us-news/2025/oct/12/china-warns-us-of-retaliation-over-trump-100-tariffs-threat\"\u003Esaid\u003C/a\u003E China would pursue “resolute measures to protect its legitimate rights and interests”. China may also renege on the TikTok deal, which could do more political damage than tit-for-tat tariffs.\u003C/p\u003E"
                  }
                }
              ]
            }
          ],
          "totalBodyBlocks": 1
        },
        "isHosted": False,
        "pillarId": "pillar/news",
        "pillarName": "News"
      }
    ]
  }
}

# Completed URL as Var
test_url = "https://content.guardianapis.com/search?from-date=2025-10-01&order-by=newest&show-fields=article&page-size=10&q=trump&show-blocks=body&api-key=test"

# API test key variable
test_key = "test"


# ===== Guardian API Tests =====

# ===== API Validation =====
# Test 1 - test_API_Key_Validation:
def test_guardian_api_class_accepts_api_key():
    """Tests: accepts API key, covers any None/empty keys"""

    client = GuardianAPI(test_key)

    assert client.api_key == test_key
    # Rejects Empty
    with pytest.raises(ValueError, match="Valid API key is required"):
        GuardianAPI(api_key="")


# ===== Search Functionality =====
# Test 2  - tests request is ordered by newest articles
@patch('src.extract.requests.get')
def test_returns_latest_articles_max(mock_get):

    client = GuardianAPI("test")
    client.search_articles("trump", "")

    called_url = mock_get.call_args[0][0]
    
    assert "order-by=newest" in called_url


# Test 3 - tests request is limited to 10 articles
@patch('src.extract.requests.get')
def test_returns_10_articles_max(mock_get):

    client = GuardianAPI("test")
    client.search_articles("trump", "")

    called_url = mock_get.call_args[0][0]

    assert "&page-size=10" in called_url


# Test 4 - search query is added to url with api key
@patch("src.extract.requests.get")
def test_search_query_added_to_url(mock_get):

    client = GuardianAPI("test")
    client.search_articles("trump","")

    called_url = mock_get.call_args[0][0]

    assert "&q=trump" in called_url


# Test 5 - api key is added to url
@patch("src.extract.requests.get")
def test_api_key_added_to_url(mock_get):

    client = GuardianAPI("test")
    client.search_articles("", "")
    called_url = mock_get.call_args[0][0]

    # Check URL has API 
    assert "&api-key=test" in called_url


# Test 5 - api key is added to url with no query
@patch("src.extract.requests.get")
def test_api_key_added_to_url_with_no_query(mock_get):

    client = GuardianAPI("test")
    # No search query added
    client.search_articles("","")
    called_url = mock_get.call_args[0][0]

    # Check URL 
    assert "&api-key=test" in called_url


# Test 6 - Article Type is added to URL - removes live blogs, opinion
@patch("src.extract.requests.get")
def test_type_article_added_to_url(mock_get):

    client = GuardianAPI("test")
    client.search_articles("","")
    called_url = mock_get.call_args[0][0]

    # Check URL 
    assert "&type=article" in called_url


# Additional Features:
# Date from search functionality
@patch('src.extract.requests.get')
def test_returns_publication_date_after_date_selected(mock_get):
    """Tests: publication date is after date_from value"""
   
    client = GuardianAPI("test")
    client.search_articles("trump", "2025-10-01")

    called_url = mock_get.call_args[0][0]

    assert "from-date=2025-10-01" in called_url


@patch('src.extract.requests.get')
def test_returns_content_preview_in_url(mock_get):
    """Tests: content preview is requested in URL"""

    client = GuardianAPI("test")
    client.search_articles("trump", "2025-10-01")
  
    # Check URL includes show-blocks=body
    called_url = mock_get.call_args[0][0]
    
    assert "&show-blocks=body" in called_url


@patch('src.extract.requests.get')
def test_returns_content_preview_max_1000_chars(mock_requests, mock_guardian_api_one_response):
    """Tests: content preview is limited to 1000 chars"""
   
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_one_response
    mock_requests.return_value = mock_response
    
    client = GuardianAPI("test")
    articles = client.search_articles("trump", "2025-10-01" )
    
    # ASSERT
    assert len(articles) == 1
    assert "contentPreview" in articles[0]
    assert len(articles[0]["contentPreview"]) == 1000


# ===== Processing of JSON Data =====
# Processses JSON to required fields.

# Test 6 - Requested fields; webPublicationDate, webTitle, webUrl all returned correctly
@patch('src.extract.requests.get')
def test_returns_one_formatted_response(mock_requests, mock_guardian_api_one_response):

    # Creates instance of a mock response for requests to access
    mock_response = Mock()
    # creates guardian_api_one as the JSON response
    mock_response.json.return_value = mock_guardian_api_one_response
    # Configures mock_requests to return mocked JSON response
    mock_requests.return_value = mock_response

    client = GuardianAPI(test_key)

    articles = client.search_articles("Warwickshire")

    expected_article = [{
        "webPublicationDate": "2014-04-17T16:00:00Z",
        "webTitle": "Charging for crutches is the first painful step towards dismantling the NHS | Kailash Chand",
        "webUrl": "https://www.theguardian.com/commentisfree/2014/apr/17/charging-crutches-dismantling-nhs-south-warwickshire-ccg",
        "contentPreview": "There is little doubt that the NHS is under huge strain from a period of sustained austerity. In this difficult economic climate it is not surprising that local NHS bodies across the country are having to make difficult choices in agonising circumstances – but we must not allow this to compromise the founding principles which have sustained our health services since its creation. South Warwickshire clinical commissioning group (CCGs) is clearly facing serious financial issues, caused by the government's failure to recognise that the NHS is struggling to cope with rising patient demand, especially from our ageing society. It is the lack of understanding of these pressures that is causing CCGs like South Warickshire to look at plans like alternative income streams. Unfortunately in that case consideration now appears to being given to introducing charging for essential medical equipment such as walking sticks, knee braces and wrist splints. Let us be under no illusion that this is a triv"}
    ]
    #assert articles == expected_article
    assert len(articles) == 1
    assert len(articles[0]["contentPreview"]) == 1000


# Test 7 - tests formatting for multiple articles
@patch('src.extract.requests.get')
def test_returns_required_fields_multiple_results(mock_requests, mock_guardian_api_multiple_responses):

    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_multiple_responses
    mock_requests.return_value = mock_response

    client = GuardianAPI(test_key)

    articles = client.search_articles("trump")

    assert len(articles) == 2
    assert len(articles[0]["contentPreview"]) == 1000
    assert len(articles[1]["contentPreview"]) == 1000


# =====Lambda Handler Tests =====

@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key'})
@patch('src.extract.requests.get')
def test_lambda_handler_adds_api_key(mock_get, _mock_boto, mock_guardian_api_one_response):
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_one_response
    mock_get.return_value = mock_response

    # Act
    event = {'search_term': 'Warickshire'}
    lambda_handler(event, None)

    assert mock_get.called
    called_url = mock_get.call_args[0][0]
    assert "&api-key=test-key" in called_url


@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key'})
@patch('src.extract.requests.get')
def test_lambda_handler_uses_search_term_from_event(mock_get, _mock_boto, mock_guardian_api_one_response):

    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_one_response
    mock_get.return_value = mock_response

    # Act
    event = {'search_term': 'Warickshire'}
    lambda_handler(event, None)

    # Assert
    called_url = mock_get.call_args[0][0]
    assert '&q=Warickshire' in called_url


@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key'})
@patch('src.extract.requests.get')
def test_lambda_handler_default_search(mock_get, _mock_boto, mock_guardian_api_one_response):

    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_one_response
    mock_get.return_value = mock_response

    # Act
    # passed empty search to trigger default search
    event = {}
    lambda_handler(event, None)

    # Assert
    called_url = mock_get.call_args[0][0]
    assert '&q=Northcoders' in called_url


@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key', 'SQS_QUEUE_URL': 'test-queue'})
@patch('src.extract.requests.get')
def test_lambda_handler_creates_sqs_client(_mock_get, mock_boto):
    # boto3 will create a mock instance of SQS
    # Arrange
    event = {'search_term': 'Warickshire'}

    # Act
    lambda_handler(event, None)

    # Assert
    mock_boto.assert_called_once_with('sqs')


@patch('src.extract.boto3.client')
@patch('src.extract.requests.get')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key', 'SQS_QUEUE_URL': 'test-queue'})
def test_lambda_handler_creates_SQS_queue(mock_get, mock_boto, mock_guardian_api_one_response):
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_one_response
    mock_get.return_value = mock_response

    event = {'search_term': 'Warickshire'}

    mock_sqs_client = Mock()
    mock_boto.return_value = mock_sqs_client

    # Act
    lambda_handler(event, None)
    call_kwargs = mock_sqs_client.send_message.call_args.kwargs

    # Assert
    assert call_kwargs['QueueUrl'] == 'test-queue'


@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key', 'SQS_QUEUE_URL': 'test-queue'})
@patch('src.extract.requests.get')
# Tests the SQS recieves & sends single message
def test_lambda_handler_sends_single_article_result_to_sqs(mock_get, mock_boto, mock_guardian_api_one_response):

    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_one_response
    mock_get.return_value = mock_response

    # Create mock SQS Client
    mock_sqs_client = Mock()
    mock_boto.return_value = mock_sqs_client

    # Act
    event = {'search_term': 'Warickshire'}
    lambda_handler(event, None)

    call_args = mock_sqs_client.send_message.call_args.kwargs
    sent_message_string = call_args['MessageBody']
    # converts string to JSON for assertions below
    sent_message = json.loads(sent_message_string)

    # this is inc. instead of hardcoding results as leads to unicoding issue.
    expected_article = mock_guardian_api_one_response['response']['results'][0]

    # Assert
    assert mock_sqs_client.send_message.call_count == 1
    assert sent_message['webPublicationDate'] == expected_article['webPublicationDate']
    assert sent_message['webTitle'] == expected_article['webTitle']
    assert sent_message['webUrl'] == expected_article['webUrl']


@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key', 'SQS_QUEUE_URL': 'test-queue'})
@patch('src.extract.requests.get')
def test_lambda_handler_sends_multiple_articles_to_sqs(mock_get, mock_boto, mock_guardian_api_multiple_responses):
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_multiple_responses
    mock_get.return_value = mock_response

    # Create mock SQS Client
    mock_sqs_client = Mock()
    mock_boto.return_value = mock_sqs_client

    # Act
    event = {'search_term': 'Trump'}
    lambda_handler(event, None)

    #calls last message
    call_args = mock_sqs_client.send_message.call_args.kwargs
    sent_message_string = call_args['MessageBody']
    # converts string to JSON for assertions below
    sent_message = json.loads(sent_message_string)
    
    # Testing for last result in API results
    expected_article = mock_guardian_api_multiple_responses['response']['results'][1]

    # Assert
    assert mock_sqs_client.send_message.call_count >= 2
    assert sent_message['webPublicationDate'] == expected_article['webPublicationDate']
    assert sent_message['webTitle'] == expected_article['webTitle']
    assert sent_message['webUrl'] == expected_article['webUrl']
    assert sent_message['contentPreview'] == expected_article['blocks']['body'][0]['bodyTextSummary'][:1000]


@patch('src.extract.boto3.client')
@patch('src.extract.requests.get')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key', 'SQS_QUEUE_URL': 'test-queue'})
def test_lambda_handler_returns_success_response(mock_get, mock_boto, mock_guardian_api_one_response):
    """Test that lambda handler returns a success response"""

    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_one_response
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    mock_sqs_client = Mock()
    mock_boto.return_value = mock_sqs_client

    # Act
    event = {'search_term': 'Warwickshire'}
    result = lambda_handler(event, None)

    # Assert
    assert result['statusCode'] == 200
    assert 'body' in result


# ===== Error Handling =====
# test_error_handling - need to define what this is.
# logger is setup


def test_lambda_handler_has_logger_setup():
    from src.extract import logger

    assert logger is not None
    assert logger.level == logging.INFO


# Test that errors are logged with "ERROR" keyword
@patch('src.extract.logger')
@patch('src.extract.GuardianAPI')
@patch('src.extract.boto3.client')
def test_lambda_handler_logs_error_on_api_failure(_mock_boto, mock_guardian_api, mock_logger):
    # Arrange
    # create a mock to make API throw exception using .side_effect -
    # Requests will deal with Exception generation when live
    mock_response = Mock()
    mock_response.search_articles.side_effect = Exception("API connection failed")
    mock_guardian_api.return_value = mock_response
    event = {'search_term': 'test'}
    context = {}

    # Check that error is logged
    with pytest.raises(Exception):
        lambda_handler(event, context)

    # Verify logger.error has text containing failure info
    mock_logger.error.assert_called()
    error_message = mock_logger.error.call_args[0][0]
    assert "failed" in error_message.lower()
    # Note - CloudWatch filters logs for "Failed"


# SQS message failure gets logged for Cloudwatch & error handling
@patch('src.extract.logger')
@patch('src.extract.GuardianAPI')
@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key', 'SQS_QUEUE_URL': 'test-queue'})
def test_lambda_handler_logs_error_on_sqs_failure(mock_boto, mock_guardian_api, mock_logger):

    # API succeeds, SQS fails
    mock_response = Mock()
    mock_response.search_articles.return_value = [
        {
            'webPublicationDate': '2025-01-01T12:00:00Z',
            'webTitle': 'Test Article',
            'webUrl': 'https://example.com',
            'contentPreview': 'Test article preview content.'
        }
    ]
    mock_guardian_api.return_value = mock_response

    mock_sqs = Mock()
    mock_sqs.send_message.side_effect = Exception("SQS queue unavailable")
    mock_boto.return_value = mock_sqs

    event = {'search_term': 'test'}
    context = {}

    with pytest.raises(Exception):
        lambda_handler(event, context)

    mock_logger.error.assert_called_once()

    error_message = mock_logger.error.call_args[0][0]
    assert "sqs queue unavailable" in error_message.lower()


# API rate & Error messages logged
# Unsure if the API throttling is needed?
@patch('src.extract.logger')
@patch('src.extract.GuardianAPI')
@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key', 'SQS_QUEUE_URL': 'test-queue'})
def test_lambda_handler_logs_api_request(_mock_boto, mock_guardian_api, mock_logger):
    mock_response = Mock()
    mock_guardian_api.return_value = mock_response
    mock_response.search_articles.return_value = [
        {
            'webPublicationDate': '2025-01-01T12:00:00Z',
            'webTitle': 'Test Article',
            'webUrl': 'https://example.com',
            'contentPreview': 'Test article preview content.'
        }
    ]

    event = {'search_term': 'test'}
    context = {}
    lambda_handler(event, context)

    # Verify API call made
    message = mock_logger.info.call_args_list[1][0]
    assert "Making Guardian API call" in message
    # Note - CloudWatch API filters logs for pattern "Making Guardian API call"



