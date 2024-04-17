export REPO=kakaoent/"$1"

export PROJECT_ID=dev-ai-project-357507
export WORKLOAD_IDENTITY_POOL_ID=dev-ai-ci-service-service-pool
export SERVICE_ACCOUNT=ai-lab-github-action

export WORKLOAD_IDENTITY_POOL_RESOURCE=`gcloud iam workload-identity-pools describe "${WORKLOAD_IDENTITY_POOL_ID}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --format="value(name)"`

gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_RESOURCE}/attribute.repository/${REPO}"


# 이 스크립트를 실행하려면 iam.serviceAccount.setIamPolicy 권한이 필요합니다.
# 그러나 prod-ai-project 프로젝트의 ai-lab@kakaoent.com 계정에는 이 권한이 없습니다.
# 따라서, prod 환경에서는 이 스크립트를 직접 실행하지 않고, 아지트를 통해 클라우드팀에 작업 요청(Workload Identity 에 GitHub Actions 사용 신규 Repository 등록)을 해야 합니다.
# 다음 가이드와 예시 요청을 참고하세요.
# https://podotree.atlassian.net/wiki/spaces/RTC/pages/3216310656/ENGR+GitHub+Actions+Goolge+Cloud#prod-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8
# https://podo.agit.in/g/300061151/wall/380886597

#export REPO=kakaoent/"$1"
#
#export PROJECT_ID=prod-ai-project
#export WORKLOAD_IDENTITY_POOL_ID=prod-ai-ci-service-pool
#export SERVICE_ACCOUNT=ai-lab-github-action
#
#export WORKLOAD_IDENTITY_POOL_RESOURCE=`gcloud iam workload-identity-pools describe "${WORKLOAD_IDENTITY_POOL_ID}" \
#  --project="${PROJECT_ID}" \
#  --location="global" \
#  --format="value(name)"`
#
#gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
#  --project="${PROJECT_ID}" \
#  --role="roles/iam.workloadIdentityUser" \
#  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_RESOURCE}/attribute.repository/${REPO}"
