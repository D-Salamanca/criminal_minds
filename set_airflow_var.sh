permissions=$(stat -c "%A" "$0")
echo ""
echo "This are the permissions of this file $permissions"

if [[ ! -x "$0" ]]; then
	echo "This file dont have the necessary permissions"
	exit 1
fi

echo ""

if [ "$AIRFLOW_HOME" != "$(pwd)" ]; then
	export AIRFLOW_HOME=$(pwd)/Dags
fi

echo "AIRFLOW HOME VARIABLE SET:"
echo ""
echo $AIRFLOW_HOME
