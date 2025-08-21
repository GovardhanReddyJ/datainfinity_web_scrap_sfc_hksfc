
import json, time, requests
from urllib.parse import urlencode, quote
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "csrf-token": "ajax:4237706342477708095",
    "cookie": '''li_sugr=ec808c60-31b8-4aca-9f4f-b7dc5355862e; bcookie="v=2&94babcab-2ace-4511-84ff-9a617537696e"; bscookie="v=1&202503070733187a4112e7-e0f8-4d4b-8240-1c67d8f0c68bAQGgjOMmGyuN2DHqc3k9-9iH5OcjrZE5"; g_state={"i_l":0}; timezone=Asia/Calcutta; li_theme=light; li_theme_set=app; _guid=450ea7f4-8ad4-443e-9b26-c9722df63b58; dfpfpt=1866da6fabf94a5b9b9ef439851fd879; aam_uuid=50052513818483297892089703602694551582; _gcl_au=1.1.894500199.1753424742.213245044.1754992072.1754992072; sdui_ver=sdui-flagship:0.1.10851+sdui-flagship.production; fid=AQFxHojARvg9AQAAAZii7ONC9qPzzCVGNsDH_oLU0zkevSqgOaaEePgPD5ycFwiCXINg1M-EZ46CLA; _uetvid=2b6aeaa0784d11f08f9e43b63b2c6ecb; gpv_pn=developer.linkedin.com%2F; s_ips=738; mbox=session^#0d1c9bec2cd44f4ca1718c01835681d9^#1755095189|PC^#0d1c9bec2cd44f4ca1718c01835681d9.41_0^#1770645329; s_tp=3521; s_tslv=1755093340288; li_rm=AQGdQfcfbn9ofwAAAZinjdLXyOVqPNARLs1kWq1DuTKEfBtnFCmcCt-jpaE_-3ePAjZOdriAdFDa8sytbMVx5FWdj77-742DTDx7tKctEal1g3oHp4PFiWDb; visit=v=1&M; liap=true; li_at=AQEDAV27UWsEC_wOAAABmKePFkQAAAGYy5uaRFYAmCl7VpRfUqVLoGblQPShZ1_mcLaE5EN5q0CfmSDQvVc9NXCDpESP4assVYWuei0tIdeguZ0QmIy62G18ZCmTblTODLOO-VxehiDAphgmL3n7PJWe; JSESSIONID=ajax:4237706342477708095; lang=v=2&lang=en-us; AnalyticsSyncHistory=AQKCZ6jT7i12gAAAAZi2odQamJeI6P99DyPYzXlvI9PxLJLcvtxF6cKFJYVdutNflIMmWLJ3IYtt8z-lxck4OQ; lms_ads=AQEDGoJSiL7-gQAAAZi2odYRuR9dgpQAmJXpG5J5L5K_GBzvfdesK632huh4NVh4-T7XSjixuYjzcNH-tEQi3m7lMHk0flWw; lms_analytics=AQEDGoJSiL7-gQAAAZi2odYRuR9dgpQAmJXpG5J5L5K_GBzvfdesK632huh4NVh4-T7XSjixuYjzcNH-tEQi3m7lMHk0flWw; fptctx2=taBcrIH61PuCVH7eNCyH0B9zcK90d%252bIeoo1r5v7Zc27UqfUqqQTrRHxFk6He6FiKeFlES9G2SENH8Cjw61vOjK7uAQqg%252bvk83ml2wGl3Jo%252fr%252bEvo63vyN1pXW1yhEhtnqHrj1x5lu9%252fCMFy1Ws9vnh6LE4yQVgrR2OfZnIudw6VMT7RSGX2jgU3rG%252fa7Jz6wAe1Kg1oHxXWmKKIM4f3018D2O4t3ROO3krVZ1YGiIsSATjrQwEM7mmu2KSMiKX%252f6b6ml8FRPCbc%252bKNEKQkO00JZpvFt5bhazOkaO%252bFkiPNtg1RGw%252bJUr0EhFfzwHOlz756VinkJfvtlC%252f1TF5mxJS25qZossBOC3DjchbtwHdefDlPsr%252feE1nxzftmNDeMkgDMMnsMSALZ65GWPcTLqWZQ%253d%253d; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C20318%7CMCMID%7C50240717373430000542147989863054740437%7CMCAAMLH-1756015584%7C12%7CMCAAMB-1756015584%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1755417984s%7CNONE%7CMCCIDH%7C-2030305590%7CvVersion%7C5.1.1; __cf_bm=f0zLcG4y9yEzbLwtJTr7m8aiBKSo7.KeHZP0cO6UGrI-1755410789-1.0.1.1-ruBWME3ag9_.FX03PC9lR5yFipTdV2vmgYV7Neeu14wtCDmiiaNUZjN5UYxLFrMB3wBu3wBWsGY0CumHH5dvoBBkSjjOeoAGRzv9zbOMAXU; UserMatchHistory=AQJozjyVYPFBBAAAAZi2o3AZZc8J3G0Vuj5XzduyZfQY7_uTIqGpd0qSayH3uy8JzUPwdjbOWwbK_ZTCxbDuCznK1M2rMMDEDjxeJ9w_xC7Mc-M4rqv_fkHli4iktb2QnFkOC2PYpFNI-igLmBkYHutblX8_OIflwMSywaaeduOULFFBUFlzzup5VzkJmd5PlCdAGzg5xwmZIMVcRV-uM0Fr8IEsA_9VdmTPGjzqqcdZHCeEo95s8BZA6kGbVAkhU1ZZHLAVJ5Gpnx2wsj_xEymsKT3s7qylOSvuCsfJnlTwYI-SmUaAIduEMoTTic3A8qgzGMQj0Q6xghUYDoFhTjvzg4qAFZmbA5w8v614BLJ-m77o5g; lidc="b=OB63:s=O:r=O:a=O:p=O:g=6509:u=2:x=1:i=1755410825:t=1755497108:v=2:sig=AQEvcvUySs4E_4-RVQc1Yn9oAb_OXWdH'''}
final_output = []


def extract_profiles(data):
    profiles = []

    if isinstance(data, dict) and 'data' in data and 'searchDashClustersByAll' in data['data']:
        clusters = data['data']['searchDashClustersByAll']

        if 'elements' in clusters:
            for element in clusters['elements']:
                if 'items' in element:
                    for item in element['items']:
                        if not isinstance(item, dict):
                            continue
                        entity_result = item.get('item', {}).get('entityResult')
                        if not isinstance(entity_result, dict):
                            continue
                        # Safely extract badge text
                        badge_text = entity_result.get('badgeText', {})
                        connection = ''
                        if isinstance(badge_text, dict):
                            connection = badge_text.get('text', '').replace('•', '').strip()

                        profile = {
                            'name': entity_result.get('title', {}).get('text', 'N/A'),
                            'position': entity_result.get('primarySubtitle', {}).get('text', 'N/A'),
                            'connection': connection,
                            'location': entity_result.get('secondarySubtitle', {}).get('text', ''),
                            'profile_url': entity_result.get('navigationUrl', ''),
                            'image_url': None
                        }

                        # Extract profile image if available
                        image_data = entity_result.get('image', {})
                        if isinstance(image_data, dict) and 'attributes' in image_data:
                            for attr in image_data['attributes']:
                                if not isinstance(attr, dict):
                                    continue

                                detail_data = attr.get('detailData', {})
                                if 'nonEntityProfilePicture' in detail_data:
                                    vector_image = detail_data['nonEntityProfilePicture'].get('vectorImage')
                                    if isinstance(vector_image, dict) and 'artifacts' in vector_image:
                                        for artifact in vector_image['artifacts']:
                                            if isinstance(artifact, dict) and artifact.get('width') == 100:
                                                root_url = vector_image.get('rootUrl', '')
                                                path = artifact.get('fileIdentifyingUrlPathSegment', '')
                                                profile['image_url'] = f"{root_url}{path}" if root_url else path
                                                break

                        profiles.append(profile)

    return profiles


def main(num, company_id, COMPANY_SLUG, headers):
    url = f"https://www.linkedin.com/voyager/api/graphql?variables=(start:{num},origin:FACETED_SEARCH,query:(flagshipSearchIntent:ORGANIZATIONS_PEOPLE_ALUMNI,queryParameters:List((key:currentCompany,value:List({company_id})),(key:resultType,value:List(ORGANIZATION_ALUMNI))),includeFiltersInResponse:true),count:20)&queryId=voyagerSearchDashClusters.5ba32757c00b31aea747c8bebb92855c"
    # url = "https://www.linkedin.com/voyager/api/graphql?variables=(start:24,origin:FACETED_SEARCH,query:(flagshipSearchIntent:ORGANIZATIONS_PEOPLE_ALUMNI,queryParameters:List((key:currentCompany,value:List(1362039)),(key:resultType,value:List(ORGANIZATION_ALUMNI))),includeFiltersInResponse:true),count:12)&queryId=voyagerSearchDashClusters.5ba32757c00b31aea747c8bebb92855c"

    response = requests.get(url, headers=headers, timeout=10)
    print("Status:", response.status_code)
    data = response.json()
    # Extract profiles
    profiles = extract_profiles(data)
    if profiles:
        final_output.extend(profiles)
        print(f"[+] Extracted {len(profiles)} profiles starting from index {num}.")
    else:
        print(f"[!] No profiles found starting from index {num}.")


if __name__ == "__main__":
    # company_id=4483
    # COMPANY_SLUG = "investec"
    company_id = 1362039
    COMPANY_SLUG = "neosoft"
    for num in range(0, 60, 20):
        print(f"[+] Fetching profiles starting from index {num}...")
        main(num, company_id, COMPANY_SLUG, headers)
        time.sleep(10)

    if final_output:
        df = pd.DataFrame(final_output)
        df.to_excel("linkedin_profiles.xlsx", index=False)
        print("[+] Data saved to linkedin_profiles.xlsx")
    else:
        print("[!] No profiles extracted.")

